# GitHub 저장소 설정 가이드

## 1단계: GitHub 저장소 생성

1. https://github.com/new 접속
2. Repository name: `pyscale`
3. Description: `AI Image Upscaler with Resource Allocation`
4. Public 선택
5. ✅ "Add a README file"
6. ✅ "Add .gitignore" → Python 선택
7. ✅ "Choose a license" → MIT License
8. Create repository 클릭

## 2단계: 로컬 설정

```bash
# Git 사용자 설정
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 저장소 클론
git clone https://github.com/YOUR_USERNAME/pyscale.git
cd pyscale
```

## 3단계: 파일 추가 및 푸시

```bash
# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial commit: Complete PyScale framework"

# 푸시
git push -u origin main
```

## 4단계: 저장소 설정

GitHub Settings에서:
- ✅ Description 추가
- ✅ Topics 추가: `image-processing`, `upscaling`, `ai`, `python`
- ✅ Website URL (선택)

## 이후 작업

```bash
# 새로운 기능 추가
git checkout -b feature/new-feature
# ... 코드 수정 ...
git add .
git commit -m "feat: Add new feature"
git push origin feature/new-feature

# Pull Request 생성 후 merge
```

## 커밋 메시지 컨벤션

```
feat:  새로운 기능
fix:   버그 수정
docs:  문서 변경
style: 코드 스타일
refactor: 리팩토링
perf:  성능 개선
test:  테스트 추가
chore: 기타 변경
```

예시:
```
git commit -m "feat: Add intelligent hybrid algorithm"
git commit -m "fix: Fix memory leak in upscaler"
git commit -m "docs: Update README"
```
