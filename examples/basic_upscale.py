"""
examples/basic_upscale.py - 기본 사용 예제

이미지를 업스케일하는 가장 간단한 방법
"""

import cv2
from src import IntelligentHybrid

# 이미지 로드
image = cv2.imread("input.jpg")
if image is None:
    print("이미지를 찾을 수 없습니다!")
    exit(1)

# 업스케일러 생성
upscaler = IntelligentHybrid(sharpness=0.3)

# 업스케일 실행
result, metrics = upscaler.upscale_safe(image, scale_factor=2.0)

# 결과 저장
cv2.imwrite("output.png", result)

# 성능 출력
print(f"✅ 완료!")
print(f"   처리 시간: {metrics.processing_time_ms:.2f}ms")
print(f"   FPS: {metrics.fps:.1f}")
print(f"   출력: {metrics.output_size}")
