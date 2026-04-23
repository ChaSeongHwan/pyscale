# ⬆ PyScale - AI 이미지 업스케일러

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)

**Lossless Scaling 스타일의 완전 모듈화된 업스케일링 프로젝트**

## ✨ 주요 기능

### 알고리즘 (8가지)
- **고전**: Nearest Neighbor, Bilinear, Bicubic, Lanczos 4
- **고급**: FSR (AMD), NIS (NVIDIA), xBR (픽셀아트)
- **AI**: Real-ESRGAN (신경망 기반)

### 하이브리드 (3가지) ⭐
- **IntelligentHybrid**: 이미지 자동 분석 → 최적 알고리즘 선택
- **MultiScaleUpscaler**: 단계적 업스케일 (2×2×2 = 8×)
- **AdaptiveResourceUpscaler**: 메모리 제약 기반 자동 조정

### 고급 기능
- 🎛️ **리소스 할당**: CPU/GPU/메모리 자동 또는 수동 조정
- 📊 **성능 모니터링**: 실시간 FPS, 메모리, CPU 추적
- 🎨 **고급 GUI**: tkinter 기반 (리소스 할당 포함)
- 📈 **벤치마크**: 알고리즘 성능 자동 비교
- 🖥️ **CLI 모드**: 배치 처리 가능

## 🚀 빠른 시작

```bash
# 1. 설치
pip install -r requirements.txt

# 2. GUI 실행
python pyscale.py

# 3. 또는 CLI 사용
python pyscale.py -i input.jpg -o output.png --scale 4
```

## 📁 프로젝트 구조

```
pyscale/
├── src/
│   ├── config/         # 설정 & 리소스 관리
│   ├── algorithms/     # 8개 알고리즘 + 3개 하이브리드
│   ├── core/          # 성능 모니터링
│   ├── ui/            # 고급 GUI
│   └── ...
├── tests/             # 테스트
├── docs/              # 문서
├── examples/          # 예제
├── pyscale.py         # 메인 진입점
├── setup.py           # 패키지 설정
└── README.md          # 이 파일
```

## 📖 문서

- [GITHUB_SETUP.md](GITHUB_SETUP.md) - GitHub 저장소 설정 가이드
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - 아키텍처 설명
- [API.md](docs/API.md) - API 문서

## 🤝 기여

Fork → Feature Branch → Pull Request 환영합니다!

## 📝 라이선스

MIT License - 자유롭게 사용 가능
