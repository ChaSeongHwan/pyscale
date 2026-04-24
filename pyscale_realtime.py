#!/usr/bin/env python3
"""
pyscale_realtime.py - PyScale 실시간 업스케일러 메인

게임, 화면, 영상을 실시간으로 업스케일링합니다.

사용법:
  python pyscale_realtime.py              # GUI 실행
  python pyscale_realtime.py --profile balanced --scale 2.0
"""

import argparse
import sys
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)


def gui_mode():
    """GUI 모드"""
    try:
        from src.ui.realtime_gui import main
        main()
    except ImportError as e:
        print(f"❌ GUI 의존성 누락: {e}")
        print("설치: pip install -r requirements.txt")
        sys.exit(1)


def cli_realtime(args):
    """CLI 실시간 모드"""
    from src.config.settings import AppConfig, ResourceProfile
    from src.capture.realtime import RealtimeCapture, CaptureRegion
    from src.algorithms.hybrid import SmartHybrid
    from src.core.realtime_processor import RealtimeProcessor
    import time
    import cv2
    
    # 프로필 선택
    profile_map = {p.name.lower(): p for p in ResourceProfile}
    profile = profile_map.get(args.profile.lower(), ResourceProfile.BALANCED)
    
    # 설정
    config = AppConfig(profile)
    config.print_config()
    
    # 캡처 영역
    if args.region:
        x, y, w, h = map(int, args.region.split(','))
        region = CaptureRegion(x, y, w, h)
    else:
        region = CaptureRegion()  # 전체 화면
    
    # 캡처 시작
    print(f"\n📺 캡처 시작: {region}")
    capture = RealtimeCapture(region=region, target_fps=args.fps)
    capture.start()
    
    # 업스케일러
    upscaler = SmartHybrid(scale=args.scale)
    
    # 처리 시작
    print(f"⚙️  업스케일링: ×{args.scale} ({args.algorithm})")
    
    frame_count = 0
    start_time = time.time()
    
    try:
        while True:
            frame = capture.get_latest_frame()
            if frame is not None:
                # 업스케일
                result, metrics = upscaler.upscale_safe(frame, args.scale)
                
                # 결과 표시
                cv2.imshow("Original", frame)
                cv2.imshow("Upscaled", result)
                
                frame_count += 1
                
                # 통계 출력 (매초)
                elapsed = time.time() - start_time
                if elapsed >= 1:
                    fps = frame_count / elapsed
                    print(f"FPS: {fps:.1f} | 처리: {metrics.time_ms:.2f}ms | 프레임: {frame_count}")
                    frame_count = 0
                    start_time = time.time()
            
            # 종료 (Q 키)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\n중지됨")
    finally:
        capture.stop()
        cv2.destroyAllWindows()


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        prog="pyscale_realtime",
        description="PyScale - 실시간 게임/화면 업스케일러"
    )
    
    # 모드 선택
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--gui", action="store_true", help="GUI 모드 (기본)")
    mode_group.add_argument("--cli", action="store_true", help="CLI 모드")
    
    # 설정 옵션
    parser.add_argument(
        "--profile",
        default="balanced",
        choices=["minimal", "light", "balanced", "performance", "maximum"],
        help="리소스 프로필 (기본: balanced)"
    )
    
    parser.add_argument(
        "--scale",
        type=float,
        default=2.0,
        help="배율 (기본: 2.0)"
    )
    
    parser.add_argument(
        "--algorithm",
        default="smart",
        choices=["smart", "bilinear", "bicubic", "lanczos", "fsr", "nis"],
        help="업스케일 알고리즘 (기본: smart)"
    )
    
    parser.add_argument(
        "--fps",
        type=int,
        default=60,
        help="목표 FPS (기본: 60)"
    )
    
    parser.add_argument(
        "--region",
        type=str,
        help="캡처 영역 (x,y,width,height)"
    )
    
    args = parser.parse_args()
    
    # 모드 결정
    if args.cli:
        cli_realtime(args)
    else:
        # GUI 모드 (기본)
        gui_mode()


if __name__ == "__main__":
    main()
