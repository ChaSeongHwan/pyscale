"""
examples/resource_allocation.py - 리소스 할당 예제

시스템에 맞는 최적의 리소스 할당
"""

import cv2
from src import AppConfig, ResourceProfile, SystemInfo
from src import IntelligentHybrid

# 시스템 정보 출력
SystemInfo.print_info()

# 리소스 프로필 선택 (자동 또는 수동)
# 자동: AppConfig()
# 수동: AppConfig(ResourceProfile.BALANCED)

config = AppConfig()  # 자동 감지
print(f"선택 프로필: {config.profile.value}")
print(f"할당 리소스:")
print(f"  CPU: {config.resource_config.cpu_threads}코어")
print(f"  메모리: {config.resource_config.memory_limit_mb}MB")
print(f"  타일: {config.resource_config.max_tile_size}×{config.resource_config.max_tile_size}px")

# 이미지 로드
image = cv2.imread("input.jpg")

# 처리 가능 여부 확인
h, w = image.shape[:2]
if config.can_process(w, h, 2.0):
    print("✅ 처리 가능\n")
    
    # 업스케일
    upscaler = IntelligentHybrid()
    result, metrics = upscaler.upscale_safe(image, 2.0)
    cv2.imwrite("output.png", result)
else:
    print("❌ 메모리 부족")
