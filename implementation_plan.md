# [구현 계획] Recipes API 개발

## 목표
사용자가 보유한 식재료 및 영양 상태를 기반으로 레시피를 추천받고 조회할 수 있는 API 엔드포인트를 구현합니다. `RecipeChefAgent`와 연동하여 AI 기반 추천을 제공합니다.

## 사용자 검토 필요 (User Review Required)
> [!NOTE]
> `RecipeChefAgent`는 이미 `backend/app/agents/recipe_chef.py`에 구현되어 있습니다. 이를 API에 연결하는 작업이 주된 내용입니다.

## 제안된 변경 사항 (Proposed Changes)

### Backend

#### [NEW] [recipes.py](file:///Users/hyunjoon/SideProjects/Nutrition/backend/app/api/recipes.py)
- **`router` 정의**: `/api/recipes` 프리픽스 사용.
- **`POST /recommend`**:
    - Input: `RecipeRecommendationRequest` (잔여 영양소, 재고 목록 등).
    - Logic: `RecipeChefAgent.process()` 호출.
    - Output: 추천 레시피 목록.
- **`GET /{recipe_id}`**:
    - DB에서 레시피 조회 (아직 DB에 레시피가 없다면 Mock 또는 DB 조회 로직 구현).

#### [MODIFY] [main.py](file:///Users/hyunjoon/SideProjects/Nutrition/backend/app/main.py)
- `recipes.router`를 `app`에 포함 (`include_router`).

## 검증 계획 (Verification Plan)

### Automated Tests
- `verify_recipes.py` 스크립트 작성 및 실행.
    - `POST /api/recipes/recommend` 호출 후 응답 구조 및 데이터 검증.
    - Gemini API 연동 확인.
