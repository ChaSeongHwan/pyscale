"""
src/config/settings.py - 설정 및 리소스 관리

실시간 업스케일러의 모든 설정을 관리합니다.
"""

import psutil
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ResourceProfile(Enum):
    """리소스 프로필"""
    MINIMAL = "극저사양"      # 1GB RAM, 1-2 코어
    LIGHT = "저사양"         # 4GB RAM, 2-4 코어
    BALANCED = "일반"        # 8GB RAM, 4-8 코어
    PERFORMANCE = "고사양"    # 16GB RAM, 8+ 코어, GPU
    MAXIMUM = "극고사양"      # 32GB+ RAM, 16+ 코어, 고성능 GPU


@dataclass
class ProfileConfig:
    """프로필별 설정"""
    target_fps: int
    default_scale: float
    default_algorithm: str
    max_resolution: tuple
    buffer_size: int


PROFILES = {
    ResourceProfile.MINIMAL: ProfileConfig(
        target_fps=30,
        default_scale=1.5,
        default_algorithm="bilinear",
        max_resolution=(1280, 720),
        buffer_size=1,
    ),
    ResourceProfile.LIGHT: ProfileConfig(
        target_fps=45,
        default_scale=1.5,
        default_algorithm="bicubic",
        max_resolution=(1600, 900),
        buffer_size=2,
    ),
    ResourceProfile.BALANCED: ProfileConfig(
        target_fps=60,
        default_scale=2.0,
        default_algorithm="smart",
        max_resolution=(1920, 1080),
        buffer_size=3,
    ),
    ResourceProfile.PERFORMANCE: ProfileConfig(
        target_fps=100,
        default_scale=2.0,
        default_algorithm="smart",
        max_resolution=(2560, 1440),
        buffer_size=4,
    ),
    ResourceProfile.MAXIMUM: ProfileConfig(
        target_fps=144,
        default_scale=2.0,
        default_algorithm="lanczos",
        max_resolution=(3840, 2160),
        buffer_size=6,
    ),
}


class SystemInfo:
    """시스템 정보"""
    
    @staticmethod
    def get_cpu_cores() -> int:
        """CPU 코어 수"""
        return psutil.cpu_count(logical=True) or 4
    
    @staticmethod
    def get_available_memory_mb() -> int:
        """사용 가능 메모리 (MB)"""
        return int(psutil.virtual_memory().available / (1024 * 1024))
    
    @staticmethod
    def has_gpu() -> bool:
        """GPU 사용 가능"""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
    
    @staticmethod
    def recommend_profile() -> ResourceProfile:
        """시스템에 맞는 프로필 추천"""
        cores = SystemInfo.get_cpu_cores()
        memory = SystemInfo.get_available_memory_mb()
        has_gpu = SystemInfo.has_gpu()
        
        if memory < 2048:
            return ResourceProfile.MINIMAL
        elif memory < 4096 or cores <= 2:
            return ResourceProfile.LIGHT
        elif memory < 8192 or cores <= 4:
            return ResourceProfile.BALANCED
        elif memory < 16384 or cores <= 8:
            return ResourceProfile.PERFORMANCE
        else:
            return ResourceProfile.MAXIMUM
    
    @staticmethod
    def print_info():
        """시스템 정보 출력"""
        print("\n" + "="*50)
        print("📊 시스템 정보")
        print("="*50)
        print(f"CPU 코어:       {SystemInfo.get_cpu_cores()}")
        print(f"메모리:          {SystemInfo.get_available_memory_mb()}MB")
        print(f"GPU 사용 가능:   {SystemInfo.has_gpu()}")
        profile = SystemInfo.recommend_profile()
        print(f"추천 프로필:     {profile.value}")
        print("="*50 + "\n")


class AppConfig:
    """애플리케이션 설정"""
    
    def __init__(self, profile: ResourceProfile = None):
        """
        초기화
        
        Args:
            profile: ResourceProfile (None = 자동 감지)
        """
        if profile is None:
            self.profile = SystemInfo.recommend_profile()
        else:
            self.profile = profile
        
        self.profile_config = PROFILES[self.profile]
        
        logger.info(f"✓ Config: {self.profile.value} 프로필")
    
    def get_target_fps(self) -> int:
        """목표 FPS"""
        return self.profile_config.target_fps
    
    def get_default_scale(self) -> float:
        """기본 배율"""
        return self.profile_config.default_scale
    
    def get_default_algorithm(self) -> str:
        """기본 알고리즘"""
        return self.profile_config.default_algorithm
    
    def get_max_resolution(self) -> tuple:
        """최대 해상도"""
        return self.profile_config.max_resolution
    
    def print_config(self):
        """설정 출력"""
        print(f"\n⚙️  {self.profile.value} 프로필 설정:")
        print(f"  FPS: {self.get_target_fps()}")
        print(f"  기본 배율: {self.get_default_scale()}×")
        print(f"  기본 알고리즘: {self.get_default_algorithm()}")
        print(f"  최대 해상도: {self.get_max_resolution()}\n")
