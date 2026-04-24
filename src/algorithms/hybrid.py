"""
src/algorithms/hybrid.py - 하이브리드 알고리즘 (3가지)

SmartHybrid, MultiStage, MemoryAware
실시간 처리에 최적화됨
"""

import cv2
import numpy as np
import logging
from .base import BaseUpscaler
from .classical import Lanczos, Bicubic, Bilinear
from .advanced import FSR, NIS, xBR

logger = logging.getLogger(__name__)


class SmartHybrid(BaseUpscaler):
    """
    스마트 하이브리드 - 프레임 특성에 따라 자동 선택
    
    실시간 처리용으로 가벼운 분석
    """
    
    def __init__(self, scale: float = 2.0):
        super().__init__("SmartHybrid", scale)
        self.algorithms = {
            'bilinear': Bilinear(scale),
            'bicubic': Bicubic(scale),
            'fsr': FSR(scale),
            'lanczos': Lanczos(scale),
        }
        self.selected_algo = 'bicubic'
    
    def _detect_frame_type(self, frame: np.ndarray) -> str:
        """프레임 타입 감지 (빠른 버전)"""
        # 작은 크기로 분석 (속도 개선)
        small = cv2.resize(frame, (160, 120))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        
        # 엣지 감지
        edges = cv2.Canny(gray, 100, 200)
        edge_ratio = np.sum(edges > 0) / edges.size
        
        # 엣지 비율에 따라 알고리즘 선택
        if edge_ratio > 0.2:
            return 'fsr'  # 게임/고에너지 콘텐츠
        elif edge_ratio > 0.1:
            return 'bicubic'  # 균형
        else:
            return 'bilinear'  # 부드러운 콘텐츠
    
    def upscale(self, frame: np.ndarray) -> np.ndarray:
        """스마트 업스케일링"""
        # 매 N번마다만 재분석 (속도 개선)
        self.frame_count = getattr(self, 'frame_count', 0) + 1
        if self.frame_count % 30 == 0:  # 30프레임마다
            self.selected_algo = self._detect_frame_type(frame)
        
        algo = self.algorithms[self.selected_algo]
        return algo.upscale(frame)


class MultiStage(BaseUpscaler):
    """
    다중 단계 업스케일 - 큰 배율을 단계적으로
    
    4× = 2×2, 8× = 2×2×2
    """
    
    def __init__(self, scale: float = 2.0):
        super().__init__("MultiStage", scale)
        self.base_algo = Bicubic(2.0)
    
    def upscale(self, frame: np.ndarray) -> np.ndarray:
        """단계적 업스케일링"""
        result = frame.copy()
        remaining = self.scale
        
        # 2×씩 반복
        while remaining > 1.0:
            current_scale = min(2.0, remaining)
            self.base_algo.scale = current_scale
            result = self.base_algo.upscale(result)
            remaining /= current_scale
        
        return result


class MemoryAware(BaseUpscaler):
    """
    메모리 인식 업스케일 - 사용 가능 메모리에 따라 조정
    """
    
    def __init__(self, scale: float = 2.0, max_memory_mb: int = 2048):
        super().__init__("MemoryAware", scale)
        self.max_memory_mb = max_memory_mb
        self.use_fast = False
    
    def upscale(self, frame: np.ndarray) -> np.ndarray:
        """메모리 기반 업스케일링"""
        h, w = frame.shape[:2]
        required_mb = w * h * self.scale * self.scale * 12 / (1024 * 1024)
        
        if required_mb > self.max_memory_mb:
            # 메모리 부족: 빠른 알고리즘 사용
            algo = Bilinear(self.scale)
        else:
            # 메모리 충분: 고품질 알고리즘 사용
            algo = Lanczos(self.scale)
        
        return algo.upscale(frame)


class FastHybrid(BaseUpscaler):
    """
    고속 하이브리드 - 실시간 60FPS+ 목표
    
    최소한의 오버헤드로 최고 속도
    """
    
    def __init__(self, scale: float = 2.0):
        super().__init__("FastHybrid", scale)
        self.algo = Bilinear(scale)
    
    def upscale(self, frame: np.ndarray) -> np.ndarray:
        """고속 업스케일링"""
        return self.algo.upscale(frame)
