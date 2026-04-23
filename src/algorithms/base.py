"""
src/algorithms/base.py - 기본 클래스

모든 업스케일러가 상속할 추상 기본 클래스
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
import time
import logging

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """성능 메트릭"""
    processing_time_ms: float = 0.0
    fps: float = 0.0
    input_size: tuple = (0, 0)
    output_size: tuple = (0, 0)
    memory_used_mb: float = 0.0


class BaseUpscaler(ABC):
    """
    기본 업스케일러 클래스
    
    모든 알고리즘이 상속해야 합니다.
    """
    
    def __init__(self, name: str = "Base", supports_gpu: bool = False):
        """
        초기화
        
        Args:
            name: 알고리즘 이름
            supports_gpu: GPU 지원 여부
        """
        self.name = name
        self.supports_gpu = supports_gpu
        self.metrics = PerformanceMetrics()
    
    @abstractmethod
    def upscale(self, image: np.ndarray, scale_factor: float, **kwargs) -> np.ndarray:
        """
        업스케일 (추상 메소드)
        
        Args:
            image: BGR numpy 배열 (H, W, 3)
            scale_factor: 배율
            
        Returns:
            np.ndarray: 업스케일 이미지
        """
        pass
    
    def upscale_safe(self, image: np.ndarray, scale_factor: float, **kwargs):
        """안전한 업스케일 (예외 처리)"""
        try:
            t0 = time.perf_counter()
            result = self.upscale(image, scale_factor, **kwargs)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            
            h, w = image.shape[:2]
            oh, ow = result.shape[:2]
            
            self.metrics.processing_time_ms = elapsed_ms
            self.metrics.fps = 1000 / elapsed_ms if elapsed_ms > 0 else 0
            self.metrics.input_size = (w, h)
            self.metrics.output_size = (ow, oh)
            
            logger.info(f"✓ {self.name}: {ow}×{oh} ({elapsed_ms:.1f}ms)")
            return result, self.metrics
            
        except Exception as e:
            logger.error(f"✗ {self.name}: {e}")
            raise
    
    def __repr__(self) -> str:
        return f"{self.name}"
