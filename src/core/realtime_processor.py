"""
src/core/realtime_processor.py - 실시간 업스케일 처리

화면 캡처 → 업스케일링 → 출력 (실시간 파이프라인)
- 비동기 처리
- 프레임 동기화
- 성능 모니터링
- 동적 품질 조정
"""

import cv2
import numpy as np
import threading
import time
import logging
from typing import Optional, Callable
from dataclasses import dataclass
from collections import deque

logger = logging.getLogger(__name__)


@dataclass
class ProcessingStats:
    """처리 통계"""
    total_fps: float = 0.0
    capture_fps: float = 0.0
    upscale_fps: float = 0.0
    output_fps: float = 0.0
    upscale_time_ms: float = 0.0
    total_time_ms: float = 0.0
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    dropped_frames: int = 0


class RealtimeProcessor:
    """
    실시간 업스케일 파이프라인
    
    흐름:
    캡처 → 큐 → 업스케일링 → 출력 → 표시
    
    특징:
    - 멀티스레드 처리
    - 프레임 드롭 최소화
    - 동적 품질 조정
    - 성능 모니터링
    """
    
    def __init__(
        self,
        capture,
        upscaler,
        output_callback: Optional[Callable] = None,
        target_fps: int = 60,
        max_queue_size: int = 2
    ):
        """
        초기화
        
        Args:
            capture: RealtimeCapture 인스턴스
            upscaler: 업스케일러 인스턴스
            output_callback: 결과 출력 콜백
            target_fps: 목표 FPS
            max_queue_size: 프레임 큐 최대 크기
        """
        self.capture = capture
        self.upscaler = upscaler
        self.output_callback = output_callback
        self.target_fps = target_fps
        self.max_queue_size = max_queue_size
        
        # 상태
        self._running = False
        self._threads: list = []
        self._lock = threading.Lock()
        
        # 프레임 큐
        self.input_queue = deque(maxlen=max_queue_size)
        self.output_queue = deque(maxlen=max_queue_size)
        
        # 통계
        self.stats = ProcessingStats()
        self._timing = deque(maxlen=30)
        self._upscale_times = deque(maxlen=30)
        
        logger.info(f"✓ RealtimeProcessor initialized")
    
    def _enqueue_frames(self):
        """캡처된 프레임을 큐에 추가"""
        while self._running:
            frame = self.capture.get_latest_frame()
            if frame is not None:
                with self._lock:
                    self.input_queue.append((time.time(), frame))
            time.sleep(0.001)  # CPU 과부하 방지
    
    def _process_frames(self):
        """프레임 업스케일링"""
        while self._running:
            try:
                with self._lock:
                    if not self.input_queue:
                        time.sleep(0.001)
                        continue
                    
                    timestamp, frame = self.input_queue.popleft()
            except IndexError:
                time.sleep(0.001)
                continue
            
            # 업스케일링
            t0 = time.perf_counter()
            try:
                upscaled, metrics = self.upscaler.upscale_safe(frame, self.upscaler.scale)
                upscale_ms = (time.perf_counter() - t0) * 1000
                
                self._upscale_times.append(upscale_ms)
                
                with self._lock:
                    self.output_queue.append((timestamp, upscaled, upscale_ms))
                
            except Exception as e:
                logger.error(f"Upscale failed: {e}")
                self.stats.dropped_frames += 1
    
    def _output_frames(self):
        """결과 출력"""
        while self._running:
            try:
                with self._lock:
                    if not self.output_queue:
                        time.sleep(0.001)
                        continue
                    
                    timestamp, frame, upscale_ms = self.output_queue.popleft()
            except IndexError:
                time.sleep(0.001)
                continue
            
            # 콜백 호출
            if self.output_callback:
                t0 = time.perf_counter()
                try:
                    self.output_callback(frame)
                except Exception as e:
                    logger.error(f"Output callback failed: {e}")
    
    def _update_stats(self):
        """통계 업데이트"""
        while self._running:
            capture_stats = self.capture.get_stats()
            
            with self._lock:
                self.stats.capture_fps = capture_stats.fps
                self.stats.upscale_fps = 1.0 / np.mean(self._upscale_times) if self._upscale_times else 0
                self.stats.upscale_time_ms = np.mean(self._upscale_times) if self._upscale_times else 0
                self.stats.total_fps = self.stats.capture_fps  # 병목: 캡처
            
            time.sleep(1)
    
    def start(self):
        """처리 시작"""
        if self._running:
            logger.warning("Processor already running")
            return
        
        self._running = True
        self.capture.start()
        
        # 스레드 시작
        threads_config = [
            ("enqueue", self._enqueue_frames),
            ("process", self._process_frames),
            ("output", self._output_frames),
            ("stats", self._update_stats),
        ]
        
        for name, func in threads_config:
            t = threading.Thread(target=func, daemon=True, name=f"pyscale-{name}")
            t.start()
            self._threads.append(t)
        
        logger.info(f"✓ Processor started with {len(self._threads)} threads")
    
    def stop(self):
        """처리 중지"""
        self._running = False
        self.capture.stop()
        
        for t in self._threads:
            t.join(timeout=2)
        
        self._threads.clear()
        logger.info("✓ Processor stopped")
    
    def get_stats(self) -> ProcessingStats:
        """통계 반환"""
        with self._lock:
            return self.stats
    
    def __enter__(self):
        """Context manager"""
        self.start()
        return self
    
    def __exit__(self, *args):
        """Context manager"""
        self.stop()
