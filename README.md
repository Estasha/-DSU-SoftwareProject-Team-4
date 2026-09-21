# 동네 진단 서비스 (dongne-jindan)

자취방·이사할 지역을 고르기 전, 주소 하나만 입력하면 **안전·생활편의·교통 접근성**을 종합 점수화해서 보여주는 웹 서비스입니다.

자세한 배경과 설계 결정은 [`docs/프로젝트_가이드.md`](./docs/프로젝트_가이드.md)를 참고하세요.

## 폴더 구조

```
dongne-jindan/
├── frontend/   # React (Vite) — 화면 UI
├── backend/    # Python + FastAPI — API 서버
├── data/       # 공공데이터 원본/전처리 스크립트
├── docs/       # 기획 문서, 요구사항표, 다이어그램
└── .github/    # PR 템플릿 등
```

## 로컬 실행 방법

### 1. 백엔드
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # 발급받은 API 키·DB 정보 입력
uvicorn app.main:app --reload
```
기본 주소: http://localhost:8000 (API 문서: http://localhost:8000/docs)

### 2. 프론트엔드
```bash
cd frontend
npm install
cp .env.example .env             # 카카오 JS 키 입력
npm run dev
```
기본 주소: http://localhost:5173

## 기술 스택

| 영역 | 기술 |
|---|---|
| 프론트엔드 | React (Vite) + Tailwind CSS |
| 백엔드 | Python + FastAPI |
| 데이터베이스 | Turso (libSQL) |
| 데이터 전처리 | Python + pandas |
| 배포 | Vercel(프론트) + Render(백엔드) |

## 팀 협업 규칙

- 브랜치: `main`(배포) ← `dev`(통합) ← `feature/역할-기능명`
- 커밋 메시지: `feat:`, `fix:`, `docs:` 접두어 사용
- 새 기능은 `dev` 대상 PR로 생성 후 팀원 1명 리뷰 → 머지

자세한 배경 설명은 `docs/프로젝트_가이드.md`의 GitHub 협업 워크플로우 섹션 참고. 아래는 실제로 따라 치면 되는 명령어 튜토리얼입니다.

## 브랜치 관계 한눈에 보기

<img src="./docs/diagrams/branch-rule.svg" alt="feature 브랜치는 dev에서 갈라져 나와 PR로 dev에 합쳐지고, dev는 주기적으로 main에 합쳐지는 구조" width="820">

feature 브랜치는 `dev`에서 갈라져 나와, 작업이 끝나면 PR을 거쳐 다시 `dev`로 합쳐집니다. `dev`에 기능이 어느 정도 쌓이면 별도 PR로 `main`에 주기적으로 병합합니다. `main`에는 feature 브랜치가 직접 닿지 않습니다.

<img src="./docs/diagrams/branch-history.svg" alt="dev가 없던 시절 main에 직행 머지되던 PR #2·#3 이후 4e75a09 지점에서 dev 브랜치가 생겼고, 지금은 feature/pm-readme-tutorial이 PR #4로 dev 병합을 기다리는 중인 이 저장소의 실제 흐름" width="920">

이 저장소에서 실제로 있었던 일: `dev`가 없던 시절엔 PR #2(`billyux/frontend-test`), PR #3(`feature/pm-docs-turso-update`)이 전부 `main`으로 직행했습니다. `4e75a09` 지점에서 `dev`를 새로 만든 뒤로는 feature 브랜치가 dev에서 갈라져 dev로 되돌아가는 방식으로 바뀌었고, PR #4가 그 첫 사례로 리뷰를 기다리는 중입니다. `main`은 아직 `4e75a09` 그대로이며, dev에 변경사항이 쌓이면 별도 PR로 옮겨질 예정입니다.

## 튜토리얼: 브랜치 생성 → 커밋 → PR

### 0. 최초 1회만: 저장소 클론 및 신원 등록
```bash
git clone https://github.com/Estasha/-DSU-SoftwareProject-Team-4.git
cd ./-DSU-SoftwareProject-Team-4   # 저장소 이름이 '-'로 시작해서 앞에 ./ 필요
git config --global user.name "본인 GitHub 아이디"
git config --global user.email "본인 GitHub 가입 이메일"
```

### 1. 작업 시작 전 `dev`를 최신 상태로
```bash
git checkout dev
git pull origin dev
```
항상 `dev`에서 새 브랜치를 파야 다른 팀원이 먼저 합친 내용을 놓치지 않습니다.

### 2. 기능 브랜치 생성
```bash
git checkout -b feature/역할-기능명
```
예: `feature/backend-search-api`, `feature/frontend-score-card`, `feature/data-crime-cleaning`

### 3. 코드 작업 + 커밋
```bash
git status                     # 뭐가 바뀌었는지 확인
git add 파일명1 파일명2         # 커밋할 파일만 정확히 지정 (git add . 은 실수로 불필요한 파일이 낄 수 있음)
git commit -m "feat: 주소 검색 API 추가"
```
의미 단위로 여러 번 커밋해도 됩니다. 메시지 접두어는 `feat:`(기능 추가) / `fix:`(버그 수정) / `docs:`(문서) / `chore:`(설정·잡일)를 사용합니다.

### 4. 원격에 브랜치 업로드
```bash
git push -u origin feature/역할-기능명
```
`-u`는 최초 1회만 필요 — 이후부터는 `git push`만 쳐도 이 브랜치로 올라갑니다.

### 5. PR(Pull Request) 생성
GitHub 웹에서 방금 푸시된 브랜치의 "Compare & pull request" 버튼을 눌러도 되고, GitHub CLI(`gh`)가 설치돼 있다면 터미널에서 바로:
```bash
gh pr create --base dev --title "feat: 주소 검색 API 추가" --body "무엇을 했는지, 어떻게 테스트했는지 작성"
```
**Base(대상 브랜치)는 반드시 `dev`**로 지정합니다. `.github/PULL_REQUEST_TEMPLATE.md` 양식(무엇을 했나요 / 어떻게 테스트했나요 / 관련 이슈 / 체크리스트)에 맞춰 작성하면 리뷰가 수월합니다.

### 6. 리뷰 및 머지
- 팀원 1명이 PR을 리뷰(Approve)하면 `dev`에 머지
- 머지 후 GitHub에서 "Delete branch" 버튼으로 원격 브랜치 정리 (또는 아래 명령어)

### 7. 머지 후 로컬 정리
```bash
git checkout dev
git pull origin dev                              # 방금 머지된 내용 받기
git branch -d feature/역할-기능명                  # 로컬 브랜치 삭제 (이미 머지된 경우만 허용됨)
git push origin --delete feature/역할-기능명        # 원격 브랜치 삭제 (웹에서 안 지웠다면)
```

### 참고: `dev` → `main` 배포
기능 브랜치는 항상 `dev`를 대상으로 PR을 올립니다. `dev`에 어느 정도 기능이 쌓이면, 팀 합의 하에 `dev → main` PR을 별도로 만들어 배포 가능한 상태로 병합합니다 (예: 매주 금요일). 이 병합은 보통 PM이나 팀 합의로 진행합니다.
