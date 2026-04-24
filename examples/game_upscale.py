"""
examples/game_upscale.py - 게임 화면 실시간 업스케일

저해상도 게임을 1.5~2배로 업스케일링합니다.
예: 1280×720 → 1920×1080

사용법:
  python examples/game_upscale.py
"""

from src.config.settings import AppConfig, ResourceProfile
from src.capture.realtime import RealtimeCapture, CaptureRegion
from src.algorithms.hybrid import SmartHybrid
from src.core.realtime_processor import RealtimeProcessor
import cv2
import logging

logging.basicConfig(level=logging.INFO)

# 게임 창의 해상도에 맞게 조정
GAME_REGION = CaptureRegion(0, 0, 1280, 720)  # 게임 영역

# 고성능 모드
config = AppConfig(ResourceProfile.PERFORMANCE)
config.print_config()

# 실시간 캡처
print("\n📺 게임 캡처 시작...")
capture = RealtimeCapture(region=GAME_REGION, target_fps=60)

# 스마트 업스케일 (게임에 최적화)
upscaler = SmartHybrid(scale=1.5)

# 처리 시작
processor = RealtimeProcessor(capture, upscaler, target_fps=60)
processor.start()

print("✓ 게임 업스케일링 시작...")
print(f"  원본: {GAME_REGION.width}×{GAME_REGION.height}")
print(f"  배율: 1.5×")
print(f"  출력: {int(GAME_REGION.width*1.5)}×{int(GAME_REGION.height*1.5)}")
print("  (종료: Q 키)\n")

try:
    frame_count = 0
    while True:
        frame = capture.get_latest_frame()
        if frame is not None:
            upscaled, metrics = upscaler.upscale_safe(frame, 1.5)
            cv2.imshow("Game Upscaled", upscaled)
            
            frame_count += 1
            if frame_count % 60 == 0:
                stats = processor.get_stats()
                print(f"FPS: {stats.total_fps:.1f} | 처리: {metrics.time_ms:.2f}ms")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\n⏹ 중지됨")

finally:
    processor.stop()
    cv2.destroyAllWindows()
    print("✓ 종료")
