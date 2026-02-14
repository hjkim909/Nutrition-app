# Nutri-Agent Flow - 개발 진행 상황

**최종 업데이트**: 2026-02-05 19:45
**개발 에이전트**: Claude Code (Sonnet 4.5)
**프로젝트 타입**: 풀스택 웹 애플리케이션 (AI 기반 영양 관리)
**AI 모델**: Google Gemini 1.5 Pro (비용 효율성)
**서버 상태**: ✅ FastAPI 실행 중 (http://localhost:8000) - PID: 86089, 86099

---

## 📋 Phase 1: 프로젝트 초기 설정 (완료 ✅)

### 완료된 작업

#### 1. 문서화
- [x] PRD.md - 프로젝트 요구사항 정의 (사용자 작성)
- [x] DATABASE_SCHEMA.md - 8개 테이블 ERD 및 쿼리 설계
- [x] README.md - 프로젝트 전체 가이드

#### 2. 프로젝트 구조
```
Nutrition/
├── backend/              ✅ FastAPI 백엔드
│   ├── app/
│   │   ├── main.py      ✅ FastAPI 애플리케이션
│   │   ├── core/        ✅ 설정, DB 연결
│   │   ├── models/      ✅ SQLAlchemy 모델 (8개)
│   │   ├── api/         ✅ API 라우터 (Meals API 완성)
│   │   ├── schemas/     ✅ Pydantic 스키마 (4개 완성)
│   │   ├── agents/      ✅ AI 에이전트 (3개 완성)
│   │   └── services/    ✅ 비즈니스 로직 (MealsService 완성)
│   ├── alembic/         ✅ 마이그레이션 설정
│   ├── venv/            ✅ Python 가상환경
│   └── requirements.txt ✅ 의존성 설치 완료
│
└── frontend/             ✅ Next.js 프론트엔드
    ├── app/             ✅ Next.js App Router
    ├── components/      ✅ UI 컴포넌트 폴더
    ├── lib/             ✅ 유틸리티
    └── package.json     ✅ 의존성 설치 완료
```

#### 3. 데이터베이스 모델 (SQLAlchemy)
완성된 8개 테이블:

| 테이블명 | 설명 | 파일 경로 |
|---------|------|----------|
| `users` | 사용자 기본 정보 | backend/app/models/users.py |
| `user_profiles` | BMR, 영양 목표, 신체 정보 | backend/app/models/users.py |
| `meals` | 식단 기록 | backend/app/models/meals.py |
| `nutrition_history` | 일별 영양소 집계 (리밸런싱) | backend/app/models/meals.py |
| `ingredients` | 식재료 마스터 데이터 | backend/app/models/ingredients.py |
| `inventory` | 사용자 냉장고 재고 | backend/app/models/inventory.py |
| `recipes` | 레시피 정보 | backend/app/models/recipes.py |
| `recipe_ingredients` | 레시피-재료 관계 (M:N) | backend/app/models/recipes.py |

**주요 관계**:
- User 1:1 UserProfile
- User 1:N Meals
- User 1:N NutritionHistory
- User 1:N Inventory
- Ingredient 1:N Inventory
- Recipe N:M Ingredient (through RecipeIngredient)

#### 4. 환경 설정
- **Backend**: Python 3.9, FastAPI 0.109, SQLAlchemy 2.0, Alembic, Google Gemini SDK
- **Frontend**: Next.js 14, React 18, Tailwind CSS 3.4, Axios
- **AI 모델**: Google Gemini 1.5 Pro (변경 완료 - 비용 효율성)
- **설정 파일**:
  - backend/.env (DATABASE_URL, GEMINI_API_KEY 등)
  - frontend/.env.example (NEXT_PUBLIC_API_URL)

---

## 🚧 Phase 2: 데이터베이스 설정 (완료 ✅)

### 완료된 작업

#### 사용자가 완료한 작업 (DOCKER_SETUP.md 3단계까지)

#### ✅ 1. PostgreSQL Docker 실행 완료
```bash
docker-compose up -d  # ✅ 완료
# Container: nutri-agent-postgres (healthy)
```

#### ✅ 2. Alembic 마이그레이션 완료
```bash
alembic revision --autogenerate -m "Initial schema"  # ✅ 완료
alembic upgrade head  # ✅ 완료
# 현재 버전: 2332ec0fb571 (head)
```

**생성된 테이블 8개**:
- users, user_profiles, meals, nutrition_history
- ingredients, inventory, recipes, recipe_ingredients

#### ✅ 3. Gemini API 키 설정 완료
```
GEMINI_API_KEY=AIzaSy*** (설정 완료)
```

---

## 📝 Phase 3: AI 에이전트 구조 설계 (완료 ✅)

### 완료된 작업

#### AI 에이전트 아키텍처
**Google Gemini 1.5 Pro 기반** (Anthropic Claude에서 변경 - 비용 효율성)

**파일 구조**:
```
backend/app/agents/
├── base.py              ✅ BaseAgent 클래스 (Gemini API 통합)
├── nutri_strategist.py  ✅ 영양소 분석 및 리밸런싱
├── recipe_chef.py       ✅ 레시피 생성 및 추천
└── inventory_agent.py   ✅ 재고 모니터링 및 알림
```

**주요 변경사항**:
- ✅ Anthropic Claude → Google Gemini 1.5 Pro로 변경
- ✅ requirements.txt 업데이트 (google-generativeai==0.8.3)
- ✅ .env 파일 업데이트 (GEMINI_API_KEY)
- ✅ BaseAgent 클래스 Gemini API 통합
- ✅ 모든 에이전트 call_gemini() 메서드로 변경

---

## 📝 Phase 3: AI 에이전트 상세 설명

### 설계할 에이전트

#### 1. Nutri-Strategist Agent
**역할**: 영양소 분석 및 리밸런싱

**Input**:
- 사용자 ID
- 오늘 날짜
- 사용자 목표 영양소 (from user_profiles)
- 오늘 섭취한 식단 (from meals)

**Process**:
- 총 섭취 영양소 계산
- 목표 대비 잔여 영양소 계산
- 편차 분석 (최근 7일 이동 평균)
- 경고 메시지 생성 (과잉/부족)

**Output**:
```json
{
  "date": "2026-02-05",
  "consumed": {
    "calories": 1200,
    "carbs_g": 150,
    "protein_g": 60,
    "fat_g": 30
  },
  "remaining": {
    "calories": 800,
    "carbs_g": 100,
    "protein_g": 90,
    "fat_g": 30
  },
  "warnings": ["Protein intake is 20% below target"],
  "recommendations": "Focus on high-protein foods for dinner"
}
```

#### 2. Recipe Chef Agent
**역할**: 레시피 생성 및 추천

**Input**:
- 잔여 영양소 (from Nutri-Strategist)
- 사용자 재고 (from inventory)
- 선호도 필터 (조리 시간, 난이도, 음식 종류)

**Process**:
- 잔여 영양소 ±10% 허용 범위 내 레시피 검색
- 재고 매칭률 계산 (가용 재료 / 필요 재료)
- AI 레시피 생성 (Claude API 호출)
- 영양소 계산 및 검증

**Output**:
```json
{
  "recommendations": [
    {
      "recipe_id": "uuid",
      "name": "Grilled Chicken Breast with Quinoa",
      "match_rate": 0.85,
      "nutrition": {
        "calories": 450,
        "carbs_g": 45,
        "protein_g": 50,
        "fat_g": 10
      },
      "missing_ingredients": ["quinoa"],
      "cooking_time_minutes": 25
    }
  ]
}
```

#### 3. Inventory Agent
**역할**: 재고 모니터링 및 알림

**Input**:
- 사용자 ID
- 현재 날짜

**Process**:
- 유통기한 임박 재료 검색 (expiry_date < TODAY + 3 days)
- 재고 부족 재료 검색 (amount_g < low_stock_threshold)
- 구매 추천 생성

**Output**:
```json
{
  "expiring_soon": [
    {"ingredient": "Milk", "expiry_date": "2026-02-07", "days_left": 2}
  ],
  "low_stock": [
    {"ingredient": "Eggs", "current_amount": 2, "threshold": 6}
  ],
  "purchase_suggestions": ["Chicken breast", "Broccoli"]
}
```

---

## 🎯 Phase 4: Backend API 개발 (진행 중 - Meals API 완료 ✅)

### 완료된 작업

#### 1. Pydantic 스키마 정의 완료 (schemas/)
**파일 구조**:
```
backend/app/schemas/
├── __init__.py        ✅ 통합 export
├── users.py           ✅ User, UserProfile 스키마
├── meals.py           ✅ Meal, NutritionBalance 스키마
├── recipes.py         ✅ Recipe, RecipeRecommendation 스키마
└── inventory.py       ✅ Inventory, InventoryAlert 스키마
```

**주요 스키마**:
- UserCreate, UserResponse, UserProfileCreate/Update/Response
- MealCreate, MealUpdate, MealResponse, NutritionBalance
- RecipeCreate, RecipeResponse, RecipeRecommendationRequest
- InventoryCreate, InventoryUpdate, InventoryAlertResponse

#### 2. Services 레이어 구현 완료 (services/)
**파일**: `meals_service.py` ✅
- `MealsService` 클래스: 식단 CRUD 및 비즈니스 로직
- **자동 nutrition_history 업데이트**: 식단 추가/수정/삭제 시 자동 계산
- **Nutri-Strategist 에이전트 연동**: 영양 밸런스 분석

**주요 메서드**:
- `create_meal()` - 식단 생성 + history 업데이트
- `get_meals()` - 필터링 지원 (날짜, 식사 타입)
- `update_meal()` - 식단 수정 + history 업데이트
- `delete_meal()` - 식단 삭제 + history 업데이트
- `get_nutrition_balance()` - AI 에이전트 호출

#### 3. Meals API 엔드포인트 완료 (api/meals.py) ✅
**구현된 엔드포인트**:
- ✅ `POST /api/meals` - 식단 기록 생성
- ✅ `GET /api/meals` - 식단 목록 조회 (날짜/타입 필터)
- ✅ `GET /api/meals/{meal_id}` - 식단 상세 조회
- ✅ `PUT /api/meals/{meal_id}` - 식단 수정
- ✅ `DELETE /api/meals/{meal_id}` - 식단 삭제
- ✅ `GET /api/meals/nutrition/balance` - **영양 밸런스 조회 (Gemini AI 연동)**

#### 4. FastAPI 메인 앱 연동 완료
- ✅ main.py에 Meals 라우터 연결
- ✅ Swagger UI 활성화 (http://localhost:8000/docs)
- ✅ CORS 설정 완료

#### 5. 의존성 문제 해결
- ✅ `email-validator==2.1.1` 패키지 추가 (EmailStr 타입 지원)

---

### 📊 현재 API 상태

**테스트 가능한 엔드포인트**:
```
http://localhost:8000/docs           ← Swagger UI
http://localhost:8000/health         ← Health Check
http://localhost:8000/api/meals      ← Meals CRUD
http://localhost:8000/api/meals/nutrition/balance  ← AI 영양 분석
```

---

### 🔜 다음 작업 (나머지 API)

#### Nutrition API (보류 - Meals API에 통합됨)
- ✅ `GET /api/meals/nutrition/balance` - 이미 구현됨
- 🔜 `POST /api/nutrition/goals` - 목표 설정 (선택)
- 🔜 `GET /api/nutrition/history` - 히스토리 조회 (선택)

#### Recipes API (다음 우선순위)
- 🔜 `POST /api/recipes/recommend` - 레시피 추천 (Recipe Chef 호출)
- 🔜 `GET /api/recipes/{recipe_id}` - 레시피 상세
- 🔜 `POST /api/recipes` - 레시피 생성

#### Inventory API (선택)
- 🔜 `GET /api/inventory` - 재고 조회
- 🔜 `POST /api/inventory` - 재고 추가
- 🔜 `GET /api/inventory/alerts` - 유통기한/재고 부족 알림

---

## 🎨 Phase 5: Frontend UI 개발 (대기 중)

### 주요 페이지

#### 1. Dashboard (/)
- 오늘의 섭취 칼로리/매크로 요약
- 목표 대비 진행률 (Progress Bar)
- 최근 식단 타임라인
- 빠른 식단 입력 버튼
- 추천 레시피 미리보기

#### 2. Meal Log (/meals)
- 식단 입력 폼 (음식 이름, 양, 시간)
- 식단 기록 리스트 (편집/삭제 가능)
- 날짜별 필터링

#### 3. Recipes (/recipes)
- 레시피 추천 카드 (Recipe Chef 결과)
- 레시피 상세 페이지 (재료, 조리법, 영양 정보)
- 레시피 필터 (난이도, 시간, 음식 종류)

#### 4. Inventory (/inventory)
- 재고 목록 (유통기한 순 정렬)
- 재고 추가/수정 폼
- 알림 배지 (유통기한 임박, 재고 부족)

---

## 🔧 기술 스택 요약

### Backend
- **Framework**: FastAPI 0.109
- **ORM**: SQLAlchemy 2.0
- **DB**: PostgreSQL 15+
- **Migrations**: Alembic 1.13
- **AI**: Anthropic Claude API
- **Auth**: JWT (python-jose)

### Frontend
- **Framework**: Next.js 14 (App Router)
- **UI**: Shadcn UI + Tailwind CSS 3.4
- **State**: Zustand 4.5
- **HTTP**: Axios 1.6
- **Charts**: Recharts 2.10

### DevOps
- **Containerization**: Docker + Docker Compose
- **Backend Deploy**: Railway / Render
- **Frontend Deploy**: Vercel

---

## 📌 다음 작업 우선순위

### ✅ 완료된 작업
1. [x] docker-compose.yml로 PostgreSQL 실행
2. [x] Alembic 마이그레이션 실행
3. [x] FastAPI 서버 실행 테스트
4. [x] Nutri-Strategist Agent 구현
5. [x] Recipe Chef Agent 구현
6. [x] Inventory Agent 구현
7. [x] Pydantic 스키마 정의 (4개 파일)
8. [x] Meals API 엔드포인트 (6개)
9. [x] Nutrition API (Meals에 통합)
10. [x] Gemini API 키 설정

### 🔜 다음 우선순위
11. [ ] **Recipes API 엔드포인트** - Recipe Chef 에이전트 연동
12. [ ] **Frontend Dashboard** - 오늘의 영양 요약
13. [ ] **Frontend Meal Log** - 식단 입력 폼
14. [ ] Inventory API 엔드포인트 (선택)
15. [ ] Frontend Recipes 페이지 (선택)

---

## 🚨 이슈 및 메모

### 현재 상태
- ✅ PostgreSQL 실행 중 (Docker)
- ✅ FastAPI 서버 실행 중 (http://localhost:8000)
- ✅ Gemini API 연동 완료
- ✅ Meals API 테스트 가능 (Swagger UI)

### 최근 해결한 이슈
- ✅ `email-validator` 패키지 누락 → 설치 완료
- ✅ Gemini API 키 설정 완료
- ✅ 포트 8000 충돌 → 서버 재시작
- ✅ `recipe_chef.py` f-string 문법 오류 → 수정 완료 (155번 라인)

### 추후 개선 사항
- [ ] 식품 영양소 데이터베이스 연동 (USDA FoodData Central API)
- [ ] 사진 인식 기능 (음식 자동 인식)
- [ ] 주간/월간 분석 리포트
- [ ] 소셜 공유 기능
- [ ] 모바일 앱 (React Native)

### 데이터 분석가 피드백
- 스키마 승인 완료 ✅
- BMR/TDEE 계산 로직은 에이전트에서 구현 예정
- 이동 평균 분석은 nutrition_history 테이블 활용

---

**마지막 업데이트**: 2026-02-05 19:45
**다음 체크포인트**: Meals API 테스트 → Recipes API 구현 또는 Frontend 개발

---

## 🔧 서버 실행 상태

### FastAPI 서버 정보
```
URL: http://localhost:8000
Swagger UI: http://localhost:8000/docs
Health Check: http://localhost:8000/health
PID: 86089 (reloader), 86099 (worker)
로그 파일: /tmp/fastapi.log
```

### 서버 관리 명령어
```bash
# 서버 상태 확인
lsof -i :8000

# 로그 확인
tail -f /tmp/fastapi.log

# 서버 종료
pkill -f uvicorn

# 서버 재시작
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 알려진 경고 (무시 가능)
- Python 3.9 버전 관련 경고 (Google API 패키지)
- OpenSSL/LibreSSL 경고 (urllib3)
- **동작에는 문제 없음**

---

## 🚀 현재 테스트 가능

### Swagger UI로 API 테스트
**URL**: http://localhost:8000/docs

**테스트 시나리오**:
1. `GET /health` - Health Check
2. `POST /api/meals` - 식단 기록 추가
3. `GET /api/meals` - 식단 목록 조회
4. `GET /api/meals/nutrition/balance` - **Gemini AI 영양 분석** ⭐

### 샘플 데이터 (식단 추가용)
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "meal_type": "breakfast",
  "food_name": "Oatmeal with Banana",
  "amount_g": 150,
  "calories": 284,
  "carbs_g": 57,
  "protein_g": 7.6,
  "fat_g": 3.8,
  "consumed_at": "2026-02-05T08:00:00"
}
```

**주의**:
- user_id를 실제 UUID로 사용 (위 샘플 사용 가능)
- nutrition/balance 호출 시 같은 user_id 사용
- Gemini API가 실제로 응답하는지 확인!
