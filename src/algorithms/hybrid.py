"""
src/algorithms/hybrid.py - 하이브리드 알고리즘 (3가지)

IntelligentHybrid, MultiScaleUpscaler, AdaptiveResourceUpscaler
"""

import cv2
import numpy as np
import logging
from .base import BaseUpscaler
from .classical import Lanczos, Bicubic, Bilinear
from .advanced import FSR, NIS, xBR

logger = logging.getLogger(__name__)


class ImageAnalyzer:
    """이미지 특성 분석"""
    
    @staticmethod
    def analyze(image: np.ndarray) -> dict:
        """
        이미지 분석
        
        Returns:
            dict: edge_strength, texture_complexity, color_diversity, noise_level
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 엣지 강도
        sobelx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        edge = np.mean(np.sqrt(sobelx**2 + sobely**2)) / 255.0
        
        # 텍스처
        low_freq = cv2.GaussianBlur(gray, (5, 5), 1.0)
        high_freq = gray.astype(np.float32) - low_freq.astype(np.float32)
        texture = np.std(high_freq) / 255.0
        
        return {
            'edge_strength': float(np.clip(edge, 0, 1)),
            'texture': float(np.clip(texture, 0, 1)),
        }
    
    @staticmethod
    def recommend_algorithm(edge: float, texture: float) -> str:
        """알고리즘 추천"""
        if edge > 0.6 or texture > 0.5:
            return "lanczos"
        elif edge > 0.3:
            return "fsr"
        else:
            return "bicubic"


class IntelligentHybrid(BaseUpscaler):
    """지능형 하이브리드 - 이미지 분석 후 최적 알고리즘 선택"""
    
    def __init__(self, sharpness: float = 0.3):
        super().__init__("IntelligentHybrid", False)
        self.sharpness = sharpness
        self.algorithms = {
            'lanczos': Lanczos(),
            'fsr': FSR(sharpness),
            'nis': NIS(sharpness),
            'bicubic': Bicubic(),
        }
    
    def upscale(self, image: np.ndarray, scale_factor: float, **kwargs) -> np.ndarray:
        """자동 분석 후 업스케일"""
        # 분석
        analysis = ImageAnalyzer.analyze(image)
        algo_name = ImageAnalyzer.recommend_algorithm(
            analysis['edge_strength'], analysis['texture']
        )
        
        logger.info(f"선택: {algo_name}")
        
        # 업스케일
        algo = self.algorithms[algo_name]
        return algo.upscale(image, scale_factor)


class MultiScaleUpscaler(BaseUpscaler):
    """다중 단계 - 큰 배율을 2×2×2로 나눔"""
    
    def __init__(self, sharpness: float = 0.3):
        super().__init__("MultiScale", False)
        self.upscaler = Lanczos()
        self.sharpness = sharpness
    
    def upscale(self, image: np.ndarray, scale_factor: float, **kwargs) -> np.ndarray:
        """단계적 업스케일"""
        result = image.copy()
        remaining = scale_factor
        
        while remaining > 1.0:
            current_scale = min(2.0, remaining)
            result = self.upscaler.upscale(result, current_scale)
            remaining /= current_scale
            logger.debug(f"단계: ×{current_scale}")
        
        return result


class AdaptiveResourceUpscaler(BaseUpscaler):
    """적응형 - 메모리 제약 기반 조정"""
    
    def __init__(self, max_memory_mb: int = 2048):
        super().__init__("AdaptiveResource", False)
        self.max_memory_mb = max_memory_mb
    
    def upscale(self, image: np.ndarray, scale_factor: float, **kwargs) -> np.ndarray:
        """메모리 검사 후 업스케일"""
        h, w = image.shape[:2]
        required_mb = w * h * scale_factor * scale_factor * 12 / (1024 * 1024)
        
        if required_mb < self.max_memory_mb:
            # 직접 처리
            algo = Lanczos()
        else:
            # 타일 처리 또는 저급 알고리즘
            algo = Bilinear()
            logger.warning("메모리 제약: 저급 알고리즘 사용")
        
        return algo.upscale(image, scale_factor)
