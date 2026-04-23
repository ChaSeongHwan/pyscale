"""
src/algorithms/advanced.py - 고급 알고리즘 (3가지)

FSR (AMD), NIS (NVIDIA), xBR (픽셀아트)
"""

import cv2
import numpy as np
from .base import BaseUpscaler


class FSR(BaseUpscaler):
    """FSR - AMD FidelityFX Super Resolution 근사"""
    
    def __init__(self, sharpness: float = 0.3):
        super().__init__("FSR (AMD)", False)
        self.sharpness = sharpness
    
    def upscale(self, image: np.ndarray, scale_factor: float, **kwargs) -> np.ndarray:
        h, w = image.shape[:2]
        new_h, new_w = int(h * scale_factor), int(w * scale_factor)
        
        # Lanczos 업스케일
        upscaled = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        
        # Y채널 선명화
        ycbcr = cv2.cvtColor(upscaled, cv2.COLOR_BGR2YCrCb)
        y = ycbcr[:, :, 0].astype(np.float32) / 255.0
        
        kernel = np.array([[-0.25, -0.25, -0.25],
                          [-0.25,  2.0,  -0.25],
                          [-0.25, -0.25, -0.25]], dtype=np.float32) * self.sharpness
        kernel[1, 1] += 1.0
        
        y_sharp = cv2.filter2D(y, -1, kernel)
        y_sharp = np.clip(y_sharp * 255, 0, 255).astype(np.uint8)
        
        ycbcr[:, :, 0] = y_sharp
        return cv2.cvtColor(ycbcr, cv2.COLOR_YCrCb2BGR)


class NIS(BaseUpscaler):
    """NIS - NVIDIA Image Scaling 근사"""
    
    def __init__(self, sharpness: float = 0.5):
        super().__init__("NIS (NVIDIA)", False)
        self.sharpness = sharpness
    
    def upscale(self, image: np.ndarray, scale_factor: float, **kwargs) -> np.ndarray:
        h, w = image.shape[:2]
        new_h, new_w = int(h * scale_factor), int(w * scale_factor)
        
        # Bicubic 업스케일
        upscaled = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
        
        # 주파수 분리 선명화
        f = upscaled.astype(np.float32) / 255.0
        radius = int(3 + self.sharpness * 2)
        base = cv2.GaussianBlur(f, (radius * 2 + 1, radius * 2 + 1), 0)
        detail = f - base
        enhanced = base + detail * (1.0 + self.sharpness * 1.5)
        
        return np.clip(enhanced * 255, 0, 255).astype(np.uint8)


class xBR(BaseUpscaler):
    """xBR - 픽셀아트 전용 2× 업스케일"""
    
    def __init__(self):
        super().__init__("xBR (픽셀아트)", False)
    
    def upscale(self, image: np.ndarray, scale_factor: float, **kwargs) -> np.ndarray:
        # 2×만 지원
        h, w = image.shape[:2]
        dst = np.zeros((h * 2, w * 2, 3), dtype=np.uint8)
        
        pad = np.pad(image, ((1, 1), (1, 1), (0, 0)), mode='edge')
        
        for j in range(h):
            for i in range(w):
                # 3×3 윈도우
                E = pad[j+1, i+1]
                A = pad[j, i]
                B = pad[j, i+1]
                C = pad[j, i+2]
                D = pad[j+1, i]
                F = pad[j+1, i+2]
                G = pad[j+2, i]
                H = pad[j+2, i+1]
                I = pad[j+2, i+2]
                
                # 간단한 xBR 로직
                e0 = e1 = e2 = e3 = E
                
                # 색상 유사도로 픽셀 선택
                dist_d = np.linalg.norm(D.astype(int) - E.astype(int))
                dist_b = np.linalg.norm(B.astype(int) - E.astype(int))
                
                if dist_b < dist_d:
                    e0 = B
                
                dst[j*2, i*2] = e0
                dst[j*2, i*2+1] = e1
                dst[j*2+1, i*2] = e2
                dst[j*2+1, i*2+1] = e3
        
        # 다른 배율은 Bicubic으로
        if scale_factor != 2.0:
            new_h, new_w = int(h * scale_factor), int(w * scale_factor)
            dst = cv2.resize(dst, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
        
        return dst
