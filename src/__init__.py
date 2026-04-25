"""
PyScale Realtime - 실시간 게임/화면 업스케일러 패키지

주요 클래스들을 쉽게 import할 수 있습니다.

사용법:
    from src import RealtimeCapture, SmartHybrid
    from src.config import AppConfig, ResourceProfile
"""

__version__ = "1.0.0"
__author__ = "PyScale Contributors"

# 주요 클래스 import
try:
    from .capture.realtime import RealtimeCapture, CaptureRegion, CaptureStats
    from .algorithms.base import BaseUpscaler, UpsampleMetrics
    from .algorithms.classical import NearestNeighbor, Bilinear, Bicubic, Lanczos
    from .algorithms.advanced import FSR, NIS, xBR
    from .algorithms.hybrid import SmartHybrid, MultiStage, MemoryAware, FastHybrid
    from .core.realtime_processor import RealtimeProcessor, ProcessingStats
    from .ui.realtime_gui import RealtimeGUI
    from .config.settings import AppConfig, ResourceProfile, SystemInfo
except ImportError as e:
    import logging
    logging.warning(f"패키지 import 실패: {e}")

__all__ = [
    # Capture
    'RealtimeCapture', 'CaptureRegion', 'CaptureStats',
    
    # Algorithms
    'BaseUpscaler', 'UpsampleMetrics',
    'NearestNeighbor', 'Bilinear', 'Bicubic', 'Lanczos',
    'FSR', 'NIS', 'xBR',
    'SmartHybrid', 'MultiStage', 'MemoryAware', 'FastHybrid',
    
    # Core
    'RealtimeProcessor', 'ProcessingStats',
    
    # UI
    'RealtimeGUI',
    
    # Config
    'AppConfig', 'ResourceProfile', 'SystemInfo',
]
