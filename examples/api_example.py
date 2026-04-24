"""
examples/api_example.py - Python API 사용 예제

자신의 코드에서 PyScale을 라이브러리로 사용하는 방법

사용법:
  python examples/api_example.py
"""

from src.capture.realtime import RealtimeCapture, CaptureRegion
from src.algorithms.hybrid import SmartHybrid
from src.config.settings import AppConfig, ResourceProfile, SystemInfo
import cv2
import logging

logging.basicConfig(level=logging.INFO)

print("\n" + "="*60)
print("PyScale API 사용 예제")
print("="*60)

# 1. 시스템 정보 확인
SystemInfo.print_info()

# 2. 설정 구성
config = AppConfig(ResourceProfile.BALANCED)
config.print_config()

# 3. 영역 선택 (게임 창, 특정 영역 등)
# 전체 화면 캡처: CaptureRegion()
# 특정 영역: CaptureRegion(x, y, width, height)
region = CaptureRegion(0, 0, 1920, 1080)

print(f"\n📍 캡처 영역: {region}")

# 4. 실시간 캡처 시작
print("\n🎬 캡처 시작...")
capture = RealtimeCapture(region=region, target_fps=60)
capture.start()

# 5. 업스케일러 생성
print("🧠 업스케일러 초기화...")
upscaler = SmartHybrid(scale=2.0)

# 6. 메인 루프
print("\n⚡ 실시간 업스케일링 처리 중...")
print("   (Q 키로 종료)\n")

frame_count = 0
try:
    while True:
        # 최신 프레임 가져오기
        frame = capture.get_latest_frame()
        
        if frame is not None:
            # 업스케일링 실행
            upscaled, metrics = upscaler.upscale_safe(frame, 2.0)
            
            # 결과 표시
            cv2.imshow("Original", frame)
            cv2.imshow("Upscaled (2×)", upscaled)
            
            frame_count += 1
            
            # 통계 출력 (매초)
            if frame_count % 60 == 0:
                capture_stats = capture.get_stats()
                print(f"📊 통계:")
                print(f"   캡처 FPS: {capture_stats.fps:.1f}")
                print(f"   업스케일 FPS: {metrics.fps:.1f}")
                print(f"   처리 시간: {metrics.time_ms:.2f}ms")
                print(f"   출력 해상도: {metrics.output_size}")
                frame_count = 0
        
        # 종료 조건
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\n⏹ 사용자가 중지함")

finally:
    # 정리
    capture.stop()
    cv2.destroyAllWindows()
    
    print("✓ 종료됨")
    print("="*60 + "\n")

# 7. 고급: 커스텀 설정
print("💡 고급 사용 예제:\n")

print("""
# 극저사양 시스템용
config = AppConfig(ResourceProfile.MINIMAL)

# 게임용 (높은 FPS)
config = AppConfig(ResourceProfile.PERFORMANCE)

# GPU 가속 (고사양)
config = AppConfig(ResourceProfile.MAXIMUM)

# 특정 영역만 캡처
region = CaptureRegion(100, 100, 800, 600)

# 다양한 알고리즘 사용
from src.algorithms.classical import Lanczos, Bicubic
upscaler = Lanczos(scale=3.0)

# Context manager 사용 (자동 정리)
with RealtimeCapture() as capture:
    while True:
        frame = capture.get_latest_frame()
        # ... 처리 ...
""")
