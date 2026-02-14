# Docker Setup Guide

## 1. Docker Desktop 설치

### macOS (Apple Silicon)
1. [Docker Desktop for Mac (Apple Silicon)](https://www.docker.com/products/docker-desktop/) 다운로드
2. DMG 파일 실행 및 Applications 폴더로 드래그
3. Docker Desktop 실행 (최초 실행 시 권한 요청)
4. 터미널에서 확인:
```bash
docker --version
docker-compose --version
```

### 예상 출력:
```
Docker version 24.0.0, build ...
Docker Compose version v2.20.0
```

---

## 2. PostgreSQL 실행

### 2.1 Docker Compose로 PostgreSQL 시작
프로젝트 루트 디렉토리에서:

```bash
# PostgreSQL 컨테이너 시작 (백그라운드)
docker-compose up -d

# 컨테이너 상태 확인
docker ps
```

**예상 출력**:
```
CONTAINER ID   IMAGE                COMMAND                  STATUS                   PORTS                    NAMES
abc123def456   postgres:15-alpine   "docker-entrypoint.s…"   Up 5 seconds (healthy)   0.0.0.0:5432->5432/tcp   nutri-agent-postgres
```

### 2.2 PostgreSQL 연결 확인
```bash
# Docker 컨테이너 내부에서 psql 실행
docker exec -it nutri-agent-postgres psql -U postgres -d nutri_agent_flow

# 연결되면 다음 명령어로 확인
\l   # 데이터베이스 목록
\q   # 종료
```

---

## 3. 데이터베이스 마이그레이션

### 3.1 백엔드 가상환경 활성화
```bash
cd backend
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

### 3.2 첫 번째 마이그레이션 생성
```bash
# Alembic이 자동으로 모델을 스캔하여 마이그레이션 파일 생성
alembic revision --autogenerate -m "Initial schema: users, meals, ingredients, recipes, inventory"
```

**생성되는 파일**: `backend/alembic/versions/YYYYMMDD_HHMM_<revision>_initial_schema.py`

### 3.3 마이그레이션 실행
```bash
# 데이터베이스에 테이블 생성
alembic upgrade head

# 현재 마이그레이션 버전 확인
alembic current
```

**예상 출력**:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> abc123def456, Initial schema
```

### 3.4 데이터베이스 확인
```bash
# psql로 테이블 확인
docker exec -it nutri-agent-postgres psql -U postgres -d nutri_agent_flow -c "\dt"
```

**예상 출력**:
```
                   List of relations
 Schema |        Name         | Type  |  Owner
--------+---------------------+-------+----------
 public | alembic_version     | table | postgres
 public | ingredients         | table | postgres
 public | inventory           | table | postgres
 public | meals               | table | postgres
 public | nutrition_history   | table | postgres
 public | recipe_ingredients  | table | postgres
 public | recipes             | table | postgres
 public | user_profiles       | table | postgres
 public | users               | table | postgres
(9 rows)
```

---

## 4. FastAPI 서버 실행

### 4.1 개발 서버 시작
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**예상 출력**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 4.2 API 확인
브라우저에서 다음 URL 접속:

- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Root**: http://localhost:8000/

---

## 5. Docker 명령어 치트시트

### 컨테이너 관리
```bash
# 컨테이너 시작
docker-compose up -d

# 컨테이너 중지
docker-compose stop

# 컨테이너 삭제 (데이터는 유지)
docker-compose down

# 컨테이너 + 볼륨 삭제 (데이터 포함)
docker-compose down -v

# 로그 확인
docker-compose logs -f postgres

# 컨테이너 재시작
docker-compose restart
```

### PostgreSQL 관리
```bash
# psql 접속
docker exec -it nutri-agent-postgres psql -U postgres -d nutri_agent_flow

# SQL 파일 실행
docker exec -i nutri-agent-postgres psql -U postgres -d nutri_agent_flow < backup.sql

# 데이터베이스 백업
docker exec nutri-agent-postgres pg_dump -U postgres nutri_agent_flow > backup.sql

# 데이터베이스 복원
docker exec -i nutri-agent-postgres psql -U postgres -d nutri_agent_flow < backup.sql
```

---

## 6. 트러블슈팅

### 문제 1: 포트 5432가 이미 사용 중
```bash
# 포트 사용 프로세스 확인
lsof -i :5432

# 기존 PostgreSQL 중지 (Homebrew 설치의 경우)
brew services stop postgresql@15
```

### 문제 2: Docker Desktop이 시작되지 않음
- Docker Desktop 재시작
- Mac 재부팅
- Docker Desktop 재설치

### 문제 3: 마이그레이션 실패
```bash
# 데이터베이스 초기화 (주의: 모든 데이터 삭제)
docker-compose down -v
docker-compose up -d

# 마이그레이션 재실행
alembic upgrade head
```

### 문제 4: 데이터베이스 연결 실패
```bash
# .env 파일 확인
cat backend/.env

# DATABASE_URL 형식 확인
# 올바른 형식: postgresql://postgres:password@localhost:5432/nutri_agent_flow
```

---

## 7. 다음 단계

Docker 및 PostgreSQL 설정이 완료되면:

1. **AI 에이전트 구현** (Nutri-Strategist, Recipe Chef, Inventory Agent)
2. **Backend API 개발** (Meals, Nutrition, Recipes, Inventory 엔드포인트)
3. **Frontend UI 개발** (Dashboard, Meal Log, Recipes 페이지)

진행 상황은 `claude.MD` 파일에서 계속 업데이트됩니다.

---

**작성일**: 2026-02-05
**버전**: 1.0
