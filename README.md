# 🎮 PyScale Realtime - 게임/화면 실시간 업스케일러

**게임, 화면, 영상을 실시간으로 업스케일링하는 고성능 시스템**

## ⚡ 주요 특징

### 실시간 처리
- 📺 **실시간 화면 캡처**: 게임, 애플리케이션 화면 직접 캡처
- ⚡ **저지연**: GPU 가속으로 지연시간 최소화
- 🔄 **지속적 처리**: 60FPS 이상 목표
- 🎯 **선택적 영역**: 특정 영역만 업스케일링

### 8가지 알고리즘
- **고전**: Nearest Neighbor, Bilinear, Bicubic, Lanczos
- **고급**: FSR (AMD), NIS (NVIDIA), xBR
- **AI**: Real-ESRGAN (신경망)

### 3가지 하이브리드 모드
- **Smart Mode**: 화면 특성에 따라 자동 선택
- **Multi-Stage**: 2×2×2 단계적 처리
- **Memory-Aware**: 메모리 제약에 맞춰 자동 조정

### 리소스 관리
- 5가지 프로필 (극저~극고사양)
- CPU/GPU 자동 할당
- 메모리 모니터링 및 최적화
- FPS 제어

## 🚀 빠른 시작

```bash
pip install -r requirements.txt
python pyscale_realtime.py
```

## 🎮 사용법

### GUI 모드 (추천)
```bash
python pyscale_realtime.py
```

설정:
1. 📍 캡처 영역 선택
2. 📊 리소스 프로필 선택
3. ⚙️ 알고리즘 선택
4. ▶️ "시작" 버튼 클릭

### CLI 모드
```bash
python pyscale_realtime.py --profile balanced --algorithm smart --region 0,0,1920,1080
```

### Python API
```python
from src.capture import RealtimeCapture
from src import SmartHybrid

capture = RealtimeCapture(region=(0, 0, 1920, 1080))
upscaler = SmartHybrid(scale=2.0)
processor = RealtimeProcessor(capture, upscaler)
processor.start()
```

## 📁 프로젝트 구조

```
pyscale_realtime/
├── src/
│   ├── capture/          # 실시간 화면 캡처
│   ├── algorithms/       # 업스케일링 알고리즘
│   ├── core/            # 성능 최적화
│   ├── ui/              # 실시간 UI
│   └── config/          # 설정 및 리소스 관리
├── examples/
│   ├── game_upscale.py
│   ├── stream_upscale.py
│   └── batch_mode.py
├── pyscale_realtime.py  # 메인 진입점
└── requirements.txt
```

## ⚙️ 설정

### 극저사양 (1GB RAM)
```python
config = AppConfig(ResourceProfile.MINIMAL)
# Bilinear 알고리즘, 30FPS, 512px 타일
```

### 일반 (8GB RAM)
```python
config = AppConfig(ResourceProfile.BALANCED)
# Smart 알고리즘, 60FPS, 1024px 타일
```

### 고사양 (16GB+ RAM, GPU)
```python
config = AppConfig(ResourceProfile.MAXIMUM)
# Real-ESRGAN, 120FPS, GPU 가속
```

## 📊 성능 목표

| 프로필 | 분해능 | FPS | 배율 | GPU |
|-------|-------|-----|------|-----|
| Minimal | 1280×720 | 30 | 1.5× | ✗ |
| Light | 1600×900 | 45 | 1.5× | ✗ |
| Balanced | 1920×1080 | 60 | 2× | ✓ |
| Performance | 2560×1440 | 100 | 2× | ✓ |
| Maximum | 3840×2160 | 120+ | 4× | ✓ |

## 🎯 사용 사례

### 게임
```
저해상도 게임 (1280×720) → 1.5× or 2× → 1920×1080 or 2560×1440
```

### 실시간 스트림
```
웹캠 (640×480) → 2× → 1280×960 (향상된 스트림)
```

### 동영상 플레이어
```
1080p 영상 → 1.5× → 1440p (업스케일 재생)
```

## 🔧 고급 설정

### 영역 선택
- 🖱️ GUI에서 마우스로 드래그해 영역 선택
- 또는 CLI: `--region x,y,width,height`

### 알고리즘 선택
- **smart**: 화면 특성에 따라 자동 선택
- **lanczos**: 최고 품질 (느림)
- **fsr**: 게임 최적화
- **nis**: 실사 최적화

### FPS 제어
- 목표 FPS 설정
- CPU/GPU 사용률에 따라 자동 조정

## 📈 모니터링

실시간 대시보드:
- 📊 FPS / 처리 시간
- 💾 메모리 사용량
- 🔥 CPU/GPU 사용률
- 🎨 선택된 알고리즘
- 📍 캡처 영역 크기

## ⚠️ 주의사항

- 🔒 일부 게임/앱은 화면 캡처 방지 (DRM)
- 💻 저사양 시스템에서는 낮은 FPS 예상
- 🌡️ GPU 온도 모니터링 권장 (장시간 사용시)

## 📝 라이선스

MIT License - 자유롭게 사용 가능

## 🤝 기여

기능 제안, 버그 리포트, Pull Request 환영합니다!

---
