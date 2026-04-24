"""
src/algorithms/classical.py - 고전 알고리즘 (4가지)

Nearest Neighbor, Bilinear, Bicubic, Lanczos
실시간 처리에 최적화됨
"""

import cv2
import numpy as np
from .base import BaseUpscaler


class NearestNeighbor(BaseUpscaler):
    """최근접 이웃 - 극도로 빠름"""
    
    def __init__(self, scale: float = 2.0):
        super().__init__("Nearest Neighbor", scale)
    
    def upscale(self, frame: np.ndarray) -> np.ndarray:
        h, w = frame.shape[:2]
        new_h, new_w = int(h * self.scale), int(w * self.scale)
        return cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_NEAREST)


class Bilinear(BaseUpscaler):
    """쌍선형 보간 - 빠르고 부드러움"""
    
    def __init__(self, scale: float = 2.0):
        super().__init__("Bilinear", scale)
    
    def upscale(self, frame: np.ndarray) -> np.ndarray:
        h, w = frame.shape[:2]
        new_h, new_w = int(h * self.scale), int(w * self.scale)
        return cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)


class Bicubic(BaseUpscaler):
    """쌍삼차 보간 - 균형잡힌 품질"""
    
    def __init__(self, scale: float = 2.0):
        super().__init__("Bicubic", scale)
    
    def upscale(self, frame: np.ndarray) -> np.ndarray:
        h, w = frame.shape[:2]
        new_h, new_w = int(h * self.scale), int(w * self.scale)
        return cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_CUBIC)


class Lanczos(BaseUpscaler):
    """Lanczos 4 - 최고 품질"""
    
    def __init__(self, scale: float = 2.0):
        super().__init__("Lanczos 4", scale)
    
    def upscale(self, frame: np.ndarray) -> np.ndarray:
        h, w = frame.shape[:2]
        new_h, new_w = int(h * self.scale), int(w * self.scale)
        return cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
