"""
src/core/performance_monitor.py - 성능 모니터링

실시간 FPS, 메모리, CPU 추적
"""

import time
import psutil
from collections import deque
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """성능 모니터링"""
    
    def __init__(self, max_history: int = 300):
        self.max_history = max_history
        self.history = deque(maxlen=max_history)
    
    def record(self, fps: float, time_ms: float, algo: str):
        """메트릭 기록"""
        self.history.append({
            'fps': fps,
            'time_ms': time_ms,
            'algorithm': algo,
            'timestamp': time.time(),
        })
    
    def get_stats(self) -> Dict:
        """통계 반환"""
        if not self.history:
            return {'avg_fps': 0, 'frame_count': 0}
        
        fps_list = [m['fps'] for m in self.history if m['fps'] > 0]
        return {
            'avg_fps': sum(fps_list) / len(fps_list) if fps_list else 0,
            'max_fps': max(fps_list) if fps_list else 0,
            'min_fps': min(fps_list) if fps_list else 0,
            'frame_count': len(self.history),
        }
    
    def print_stats(self):
        """통계 출력"""
        stats = self.get_stats()
        print(f"\n📊 성능")
        print(f"  평균 FPS: {stats['avg_fps']:.1f}")
        print(f"  프레임: {stats['frame_count']}")
        print()


class SystemResourceMonitor:
    """시스템 리소스 모니터링"""
    
    @staticmethod
    def get_cpu_percent() -> float:
        """CPU 사용률"""
        return psutil.cpu_percent(interval=0.1)
    
    @staticmethod
    def get_memory_mb() -> Dict[str, float]:
        """메모리 정보"""
        mem = psutil.virtual_memory()
        return {
            'total': mem.total / (1024 * 1024),
            'available': mem.available / (1024 * 1024),
            'used': mem.used / (1024 * 1024),
            'percent': mem.percent,
        }
    
    @staticmethod
    def print_status():
        """시스템 상태 출력"""
        cpu = SystemResourceMonitor.get_cpu_percent()
        mem = SystemResourceMonitor.get_memory_mb()
        
        print(f"\n📈 시스템")
        print(f"  CPU: {cpu:.1f}%")
        print(f"  메모리: {mem['used']:.0f}/{mem['total']:.0f} MB")
        print()
