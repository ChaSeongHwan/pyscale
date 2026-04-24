"""
examples/stream_upscale.py - 스트림/웹캠 업스케일링

웹캠이나 실시간 스트림을 2배로 업스케일링합니다.
예: 640×480 → 1280×960

사용법:
  python examples/stream_upscale.py
"""

from src.config.settings import AppConfig, ResourceProfile
from src.capture.realtime import RealtimeCapture
from src.algorithms.hybrid import FastHybrid
from src.core.realtime_processor import RealtimeProcessor
import cv2
import logging
import time

logging.basicConfig(level=logging.INFO)

# 저사양 모드 (스트림용 - 빠른 처리)
config = AppConfig(ResourceProfile.LIGHT)
config.print_config()

# 실시간 캡처
print("\n📹 화면 캡처 시작...")
capture = RealtimeCapture(target_fps=30)

# 고속 업스케일 (스트림 용)
upscaler = FastHybrid(scale=2.0)

# 처리 시작
processor = RealtimeProcessor(capture, upscaler, target_fps=30)
processor.start()

print("✓ 스트림 업스케일링 시작...")
print(f"  배율: 2.0×")
print(f"  FPS: 30")
print("  (종료: Q 키)\n")

try:
    frame_count = 0
    start_time = time.time()
    
    while True:
        frame = capture.get_latest_frame()
        if frame is not None:
            upscaled, metrics = upscaler.upscale_safe(frame, 2.0)
            cv2.imshow("Stream Upscaled", upscaled)
            
            frame_count += 1
            
            # 1초마다 통계 출력
            elapsed = time.time() - start_time
            if elapsed >= 1:
                print(f"FPS: {metrics.fps:.1f} | 처리: {metrics.time_ms:.2f}ms | 해상도: {metrics.output_size}")
                frame_count = 0
                start_time = time.time()
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\n⏹ 중지됨")

finally:
    processor.stop()
    cv2.destroyAllWindows()
    print("✓ 종료")
