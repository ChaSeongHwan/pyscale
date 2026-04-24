"""
src/capture/realtime.py - 실시간 화면 캡처

게임, 애플리케이션, 데스크톱 화면을 실시간으로 캡처합니다.
- mss (초고속 캡처)
- 비동기 처리 (threading)
- 프레임 버퍼링
- FPS 제어
"""

import mss
import numpy as np
import threading
import time
import logging
from typing import Optional, Callable, Tuple
from dataclasses import dataclass
from collections import deque

logger = logging.getLogger(__name__)


@dataclass
class CaptureRegion:
    """캡처 영역 정의"""
    x: int = 0
    y: int = 0
    width: int = 1920
    height: int = 1080
    
    @property
    def as_dict(self) -> dict:
        """mss 형식으로 변환"""
        return {"top": self.y, "left": self.x, "width": self.width, "height": self.height}
    
    def __repr__(self) -> str:
        return f"Region({self.x},{self.y} {self.width}×{self.height})"


@dataclass
class CaptureStats:
    """캡처 통계"""
    fps: float = 0.0
    frame_count: int = 0
    dropped_frames: int = 0
    avg_time_ms: float = 0.0
    memory_mb: float = 0.0


class RealtimeCapture:
    """
    실시간 화면 캡처 엔진
    
    특징:
    - 초고속 캡처 (mss)
    - 비동기 처리
    - 프레임 버퍼링
    - FPS 제어
    - 영역 선택 지원
    """
    
    def __init__(
        self,
        region: Optional[CaptureRegion] = None,
        target_fps: int = 60,
        buffer_size: int = 3
    ):
        """
        초기화
        
        Args:
            region: 캡처 영역 (None = 전체 화면)
            target_fps: 목표 FPS
            buffer_size: 프레임 버퍼 크기
        """
        self.region = region or CaptureRegion()
        self.target_fps = target_fps
        self.buffer_size = buffer_size
        
        # 상태
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        
        # 프레임 버퍼
        self.frame_buffer = deque(maxlen=buffer_size)
        self.current_frame: Optional[np.ndarray] = None
        
        # 통계
        self.stats = CaptureStats()
        self._frame_count = 0
        self._start_time = time.time()
        self._time_list = deque(maxlen=30)
        
        # 콜백
        self._on_frame_callback: Optional[Callable] = None
        
        logger.info(f"✓ RealtimeCapture initialized: {self.region}")
    
    def set_region(self, region: CaptureRegion):
        """캡처 영역 변경"""
        self.region = region
        logger.info(f"Region changed: {region}")
    
    def set_target_fps(self, fps: int):
        """목표 FPS 변경"""
        self.target_fps = fps
        logger.info(f"Target FPS changed: {fps}")
    
    def get_monitors(self) -> list:
        """모니터 목록 반환"""
        try:
            with mss.mss() as sct:
                return sct.monitors[1:]  # 0번은 전체 화면
        except Exception as e:
            logger.error(f"Failed to get monitors: {e}")
            return []
    
    def _capture_frame(self) -> Optional[np.ndarray]:
        """한 프레임 캡처"""
        try:
            with mss.mss() as sct:
                shot = sct.grab(self.region.as_dict)
                # BGRA → BGR
                frame = np.array(shot)
                frame = frame[:, :, :3]  # BGR만 추출
                return cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR) if frame.shape[2] == 4 else frame
        except Exception as e:
            logger.error(f"Capture failed: {e}")
            return None
    
    def _capture_loop(self):
        """캡처 루프 (별도 스레드에서 실행)"""
        interval = 1.0 / self.target_fps
        
        while self._running:
            t0 = time.time()
            
            # 프레임 캡처
            frame = self._capture_frame()
            if frame is not None:
                with self._lock:
                    self.current_frame = frame
                    self.frame_buffer.append(frame)
                
                # 콜백 호출
                if self._on_frame_callback:
                    self._on_frame_callback(frame)
            
            # FPS 계산
            elapsed = time.time() - t0
            self._time_list.append(elapsed)
            self._frame_count += 1
            
            if len(self._time_list) > 0:
                self.stats.avg_time_ms = np.mean(self._time_list) * 1000
                self.stats.fps = 1.0 / np.mean(self._time_list)
                self.stats.frame_count = self._frame_count
            
            # 대기
            sleep_time = interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    def start(self, on_frame: Optional[Callable] = None):
        """캡처 시작"""
        if self._running:
            logger.warning("Capture already running")
            return
        
        self._on_frame_callback = on_frame
        self._running = True
        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()
        logger.info("✓ Capture started")
    
    def stop(self):
        """캡처 중지"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("✓ Capture stopped")
    
    def get_latest_frame(self) -> Optional[np.ndarray]:
        """최신 프레임 반환"""
        with self._lock:
            return self.current_frame.copy() if self.current_frame is not None else None
    
    def get_stats(self) -> CaptureStats:
        """통계 반환"""
        return self.stats
    
    def __enter__(self):
        """Context manager 지원"""
        self.start()
        return self
    
    def __exit__(self, *args):
        """Context manager 지원"""
        self.stop()


# OpenCV import (선택적)
try:
    import cv2
except ImportError:
    cv2 = None
    logger.warning("OpenCV not available - color conversion disabled")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # 테스트: 5초간 캡처
    capture = RealtimeCapture(target_fps=30)
    capture.start()
    
    for i in range(5):
        frame = capture.get_latest_frame()
        stats = capture.get_stats()
        if frame is not None:
            print(f"Frame {i}: {frame.shape} @ {stats.fps:.1f} FPS")
        time.sleep(1)
    
    capture.stop()
    print(f"Total frames: {stats.frame_count}")
