# 🚀 Nutri-Agent Flow - 시작 가이드

AI 기반 영양 관리 시스템을 시작하는 방법입니다.

---

## 📦 현재 상태

✅ **완료된 작업**:
- 프로젝트 구조 생성
- Backend 환경 설정 (FastAPI + SQLAlchemy)
- Frontend 환경 설정 (Next.js + Tailwind CSS)
- 데이터베이스 모델 8개 생성
- Docker Compose 설정 준비

⏳ **다음 작업**:
- Docker Desktop 설치
- PostgreSQL 데이터베이스 실행
- 데이터베이스 마이그레이션

---

## 🎯 지금 해야 할 일

### 1단계: Docker Desktop 설치 (필수)

**macOS (Apple Silicon)**:
1. https://www.docker.com/products/docker-desktop/ 방문
2. "Docker Desktop for Mac (Apple Silicon)" 다운로드
3. DMG 파일 실행 → Applications 폴더로 드래그
4. Docker Desktop 실행 (최초 권한 요청 승인)

**확인**:
```bash
docker --version
docker-compose --version
```

---

### 2단계: PostgreSQL 실행

프로젝트 루트 디렉토리에서:

```bash
# PostgreSQL 컨테이너 시작
docker-compose up -d

# 상태 확인 (healthy 표시 확인)
docker ps
```

---

### 3단계: 데이터베이스 마이그레이션

```bash
cd backend
source venv/bin/activate
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

---

### 4단계: 서버 실행

**Backend**:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```
→ http://localhost:8000/docs

**Frontend** (새 터미널):
```bash
cd frontend
npm run dev
```
→ http://localhost:3000

---

## 📚 주요 문서

- **DOCKER_SETUP.md** - Docker 설치 및 DB 설정 상세 가이드
- **claude.MD** - 개발 진행 상황 및 다음 단계
- **DATABASE_SCHEMA.md** - 데이터베이스 ERD 및 쿼리
- **PRD.md** - 프로젝트 요구사항 정의
- **README.md** - 프로젝트 전체 개요

---

## 🆘 문제 해결

### PostgreSQL 연결 안 됨
```bash
# Docker 컨테이너 재시작
docker-compose restart

# 로그 확인
docker-compose logs -f postgres
```

### 마이그레이션 실패
```bash
# 데이터베이스 초기화 (주의: 데이터 삭제됨)
docker-compose down -v
docker-compose up -d
alembic upgrade head
```

---

## 📞 다음 단계

Docker 설정 완료 후:
1. AI 에이전트 구현 (Nutri-Strategist, Recipe Chef)
2. Backend API 개발
3. Frontend UI 개발

**진행 상황 추적**: `claude.MD` 파일 참조

---

**업데이트**: 2026-02-05
**개발**: Claude Code
