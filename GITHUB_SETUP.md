# 🚀 GitHub 저장소 설정 가이드

## 1단계: GitHub 저장소 생성

### 웹사이트에서 생성

1. https://github.com/new 접속
2. **Repository name**: `pyscale`
3. **Description**: `Real-time game and screen upscaler with AI`
4. **Public** 선택
5. ✅ "Add a README file"
6. ✅ "Add .gitignore" → **Python** 선택
7. ✅ "Choose a license" → **MIT License**
8. **Create repository** 클릭

## 2단계: 로컬 설정

### Git 사용자 설정

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 저장소 클론

```bash
git clone https://github.com/YOUR_USERNAME/pyscale.git
cd pyscale
```

## 3단계: 파일 추가 및 푸시

### 모든 파일 추가

```bash
git add .
```

### 커밋

```bash
git commit -m "Initial commit: PyScale realtime upscaler framework"
```

### 푸시

```bash
git push -u origin main
```

## 4단계: 저장소 설정 완료

GitHub 저장소 설정 (Settings):

1. **Description** 추가
   - "Real-time game and screen upscaler with AI"

2. **Topics** 추가
   - `image-processing`
   - `upscaling`
   - `real-time`
   - `game`
   - `ai`
   - `python`

3. **Website** (선택)
   - 블로그나 프로젝트 웹사이트 URL

4. **Branch protection** (선택)
   - Main 브랜치 보호

## 5단계: 첫 배포

### 버전 태그 생성

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### Release 생성

GitHub Releases에서:
1. "Create a new release" 클릭
2. Tag version: `v1.0.0`
3. Release title: `PyScale 1.0.0 - Real-time Upscaler`
4. Description 작성
5. "Publish release" 클릭

## 이후 작업

### 새 기능 추가

```bash
# 새 브랜치 생성
git checkout -b feature/new-algorithm

# 코드 수정 및 커밋
git add .
git commit -m "feat: Add new upscaling algorithm"

# 푸시
git push origin feature/new-algorithm
```

### Pull Request

GitHub 웹사이트에서:
1. "Compare & pull request" 클릭
2. 제목과 설명 작성
3. "Create pull request" 클릭
4. 리뷰 후 merge

## 커밋 메시지 규칙

```
feat:    새로운 기능 추가
fix:     버그 수정
docs:    문서 변경
style:   코드 스타일 (기능 변화 없음)
refactor: 코드 리팩토링
perf:    성능 개선
test:    테스트 추가
chore:   빌드/의존성 등 변경
```

### 예시

```bash
git commit -m "feat: Add FSR algorithm for game upscaling"
git commit -m "fix: Fix memory leak in realtime processor"
git commit -m "docs: Update README with API examples"
git commit -m "perf: Optimize frame buffer for lower latency"
```

## 📚 추가 자료

### GitHub 가이드
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Documentation](https://docs.github.com)

### Git 명령어

```bash
# 현재 상태 확인
git status

# 최근 커밋 수정
git commit --amend

# 마지막 커밋 되돌리기
git reset --soft HEAD~1

# 브랜치 목록
git branch -a

# 원격 저장소와 동기화
git pull origin main
```

## ✅ 체크리스트

- [ ] GitHub 계정 생성
- [ ] 저장소 생성
- [ ] Git 로컬 설정
- [ ] 저장소 클론
- [ ] 파일 추가 및 푸시
- [ ] Description 작성
- [ ] Topics 추가
- [ ] 첫 배포 (Release v1.0.0)

---

**축하합니다! 이제 GitHub에서 프로젝트를 관리할 수 있습니다!** 🎉
