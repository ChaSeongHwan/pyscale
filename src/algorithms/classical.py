"""
src/algorithms/classical.py - 고전 알고리즘 (4가지)

Nearest Neighbor, Bilinear, Bicubic, Lanczos 4
"""

import cv2
import numpy as np
from .base import BaseUpscaler


class NearestNeighbor(BaseUpscaler):
    """최근접 이웃 - 극도로 빠름"""
    
    def __init__(self):
        super().__init__("Nearest Neighbor", False)
    
    def upscale(self, image: np.ndarray, scale_factor: float, **kwargs) -> np.ndarray:
        h, w = image.shape[:2]
        new_h, new_w = int(h * scale_factor), int(w * scale_factor)
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_NEAREST)


class Bilinear(BaseUpscaler):
    """쌍선형 보간"""
    
    def __init__(self):
        super().__init__("Bilinear", False)
    
    def upscale(self, image: np.ndarray, scale_factor: float, **kwargs) -> np.ndarray:
        h, w = image.shape[:2]
        new_h, new_w = int(h * scale_factor), int(w * scale_factor)
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)


class Bicubic(BaseUpscaler):
    """쌍삼차 보간"""
    
    def __init__(self):
        super().__init__("Bicubic", False)
    
    def upscale(self, image: np.ndarray, scale_factor: float, **kwargs) -> np.ndarray:
        h, w = image.shape[:2]
        new_h, new_w = int(h * scale_factor), int(w * scale_factor)
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)


class Lanczos(BaseUpscaler):
    """Lanczos 4 - 최고 품질"""
    
    def __init__(self):
        super().__init__("Lanczos 4", False)
    
    def upscale(self, image: np.ndarray, scale_factor: float, **kwargs) -> np.ndarray:
        h, w = image.shape[:2]
        new_h, new_w = int(h * scale_factor), int(w * scale_factor)
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
