"""
src/config/config.py - 설정 및 리소스 관리

리소스 프로필, 시스템 정보, 업스케일 설정을 관리합니다.
"""

import psutil
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ResourceProfile(Enum):
    """리소스 프로필"""
    MINIMAL = "극저사양"
    LIGHT = "저사양"
    BALANCED = "일반"
    PERFORMANCE = "고사양"
    MAXIMUM = "극고사양"


@dataclass
class ResourceConfig:
    """리소스 설정"""
    cpu_threads: int
    gpu_enabled: bool
    memory_limit_mb: int
    max_tile_size: int
    parallel_upscales: int


# 프로필별 설정
PROFILES = {
    ResourceProfile.MINIMAL: ResourceConfig(1, False, 512, 256, 1),
    ResourceProfile.LIGHT: ResourceConfig(2, False, 1024, 512, 1),
    ResourceProfile.BALANCED: ResourceConfig(4, True, 2048, 1024, 2),
    ResourceProfile.PERFORMANCE: ResourceConfig(8, True, 4096, 2048, 4),
    ResourceProfile.MAXIMUM: ResourceConfig(16, True, 8192, 4096, 8),
}


class SystemInfo:
    """시스템 정보"""
    
    @staticmethod
    def get_cpu_count() -> int:
        """CPU 코어 수"""
        return psutil.cpu_count(logical=True) or 4
    
    @staticmethod
    def get_memory_mb() -> int:
        """사용 가능 메모리 (MB)"""
        return int(psutil.virtual_memory().available / (1024 * 1024))
    
    @staticmethod
    def recommend_profile() -> ResourceProfile:
        """최적 프로필 추천"""
        cpu = SystemInfo.get_cpu_count()
        mem = SystemInfo.get_memory_mb()
        
        if cpu <= 2 or mem < 2048:
            return ResourceProfile.LIGHT if mem >= 1024 else ResourceProfile.MINIMAL
        elif cpu <= 4 or mem < 8192:
            return ResourceProfile.BALANCED
        elif cpu <= 8 or mem < 16384:
            return ResourceProfile.PERFORMANCE
        else:
            return ResourceProfile.MAXIMUM
    
    @staticmethod
    def print_info():
        """시스템 정보 출력"""
        print(f"\n📊 시스템")
        print(f"  CPU: {SystemInfo.get_cpu_count()}코어")
        print(f"  메모리: {SystemInfo.get_memory_mb()}MB")
        print(f"  추천: {SystemInfo.recommend_profile().value}\n")


@dataclass
class UpscaleConfig:
    """업스케일 설정"""
    scale_factor: float = 2.0
    algorithm: str = "hybrid"
    sharpness: float = 0.3
    quality_mode: str = "balanced"


class AppConfig:
    """메인 설정 클래스"""
    
    def __init__(self, profile: Optional[ResourceProfile] = None):
        """
        초기화
        
        Args:
            profile: ResourceProfile (None이면 자동 감지)
        """
        if profile is None:
            self.profile = SystemInfo.recommend_profile()
        else:
            self.profile = profile
        
        self.resource_config = PROFILES[self.profile]
        self.upscale_config = UpscaleConfig()
        
        logger.info(f"✓ Config: {self.profile.value} 프로필")
    
    def set_profile(self, profile: ResourceProfile):
        """프로필 변경"""
        self.profile = profile
        self.resource_config = PROFILES[profile]
        logger.info(f"✓ 프로필 변경: {profile.value}")
    
    def can_process(self, width: int, height: int, scale: float) -> bool:
        """처리 가능 여부 확인"""
        required_mb = width * height * scale * scale * 12 / (1024 * 1024)
        available_mb = SystemInfo.get_memory_mb()
        return required_mb < available_mb
