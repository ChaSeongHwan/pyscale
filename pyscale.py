#!/usr/bin/env python3
"""
PyScale - AI 이미지 업스케일러
메인 진입점 (CLI/GUI 모드)
"""

import argparse
import sys
import logging
from pathlib import Path

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def cli_upscale(args):
    """CLI 모드: 이미지 업스케일"""
    import cv2
    from src.algorithms.hybrid import IntelligentHybrid
    
    # 입력 검증
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 파일 없음: {args.input}")
        sys.exit(1)
    
    # 이미지 로드
    image = cv2.imread(str(input_path))
    if image is None:
        print(f"❌ 로드 실패: {args.input}")
        sys.exit(1)
    
    h, w = image.shape[:2]
    print(f"\n📸 입력: {w}×{h}")
    
    # 업스케일
    try:
        upscaler = IntelligentHybrid(sharpness=args.sharpness)
        result, metrics = upscaler.upscale_safe(image, args.scale)
        
        # 출력 경로 결정
        output_path = Path(args.output) if args.output else \
            input_path.parent / f"{input_path.stem}_x{args.scale}{input_path.suffix}"
        
        cv2.imwrite(str(output_path), result)
        out_h, out_w = result.shape[:2]
        
        print(f"✅ 완료!")
        print(f"   출력: {output_path}")
        print(f"   해상도: {out_w}×{out_h}")
        print(f"   시간: {metrics.processing_time_ms:.2f}ms\n")
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        sys.exit(1)


def gui_mode():
    """GUI 모드 실행"""
    try:
        from src.ui.advanced_gui import AdvancedGUI
        logger.info("GUI 시작...")
        app = AdvancedGUI()
        app.mainloop()
    except ImportError:
        print("❌ GUI 의존성 누락. 'pip install -r requirements.txt' 실행")
        sys.exit(1)


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        prog="pyscale",
        description="PyScale - AI 이미지 업스케일러"
    )
    
    # 모드
    parser.add_argument("-i", "--input", help="입력 이미지 경로")
    parser.add_argument("-o", "--output", help="출력 이미지 경로")
    parser.add_argument("--scale", type=float, default=2.0, help="배율 (기본: 2.0)")
    parser.add_argument("--sharpness", type=float, default=0.3, help="선명도 (0.0~1.0)")
    
    args = parser.parse_args()
    
    # 실행 모드 결정
    if args.input:
        cli_upscale(args)
    else:
        gui_mode()


if __name__ == "__main__":
    main()
