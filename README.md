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

자세한 워크플로우는 `docs/프로젝트_가이드.md`의 GitHub 협업 워크플로우 섹션 참고.
