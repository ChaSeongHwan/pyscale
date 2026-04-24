"""
src/algorithms/base.py - 기본 업스케일러

실시간 처리를 위한 최적화된 기본 클래스
"""

from abc import ABC, abstractmethod
import numpy as np
import time
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class UpsampleMetrics:
    """업스케일 메트릭"""
    time_ms: float = 0.0
    fps: float = 0.0
    input_size: tuple = (0, 0)
    output_size: tuple = (0, 0)


class BaseUpscaler(ABC):
    """실시간 업스케일러 기본 클래스"""
    
    def __init__(self, name: str = "BaseUpscaler", scale: float = 2.0):
        """
        초기화
        
        Args:
            name: 알고리즘 이름
            scale: 배율 (1.5, 2.0, 3.0, 4.0 등)
        """
        self.name = name
        self.scale = scale
        self.metrics = UpsampleMetrics()
    
    @abstractmethod
    def upscale(self, frame: np.ndarray) -> np.ndarray:
        """
        업스케일
        
        Args:
            frame: BGR numpy 배열 (H, W, 3, uint8)
            
        Returns:
            np.ndarray: 업스케일된 프레임
        """
        pass
    
    def upscale_safe(self, frame: np.ndarray, scale: float):
        """안전한 업스케일"""
        try:
            t0 = time.perf_counter()
            self.scale = scale  # 배율 업데이트
            result = self.upscale(frame)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            
            h, w = frame.shape[:2]
            oh, ow = result.shape[:2]
            
            self.metrics.time_ms = elapsed_ms
            self.metrics.fps = 1000 / elapsed_ms if elapsed_ms > 0 else 0
            self.metrics.input_size = (w, h)
            self.metrics.output_size = (ow, oh)
            
            return result, self.metrics
        except Exception as e:
            logger.error(f"✗ {self.name}: {e}")
            raise
    
    def __repr__(self) -> str:
        return f"{self.name}(×{self.scale})"
