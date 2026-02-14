# Database Schema - Nutri-Agent Flow

## ERD Overview
```
users
  ├── user_profiles (1:1)
  ├── meals (1:N)
  ├── inventory (1:N)
  └── nutrition_history (1:N)

ingredients (master data)
  └── inventory (1:N)

recipes
  └── recipe_ingredients (N:M with ingredients)
```

---

## Table Definitions

### 1. users
사용자 기본 정보

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

---

### 2. user_profiles
사용자의 신체 정보 및 영양 목표

```sql
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE REFERENCES users(id) ON DELETE CASCADE,

    -- 신체 정보 (BMR 계산용)
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL, -- male, female
    height_cm DECIMAL(5, 2) NOT NULL,
    weight_kg DECIMAL(5, 2) NOT NULL,
    activity_level VARCHAR(20) NOT NULL, -- sedentary, lightly_active, moderately_active, very_active

    -- 계산된 BMR 및 목표
    bmr_kcal INT NOT NULL, -- Basal Metabolic Rate
    tdee_kcal INT NOT NULL, -- Total Daily Energy Expenditure

    -- 일일 목표 영양소 (g)
    target_calories INT NOT NULL,
    target_carbs_g DECIMAL(10, 2) NOT NULL,
    target_protein_g DECIMAL(10, 2) NOT NULL,
    target_fat_g DECIMAL(10, 2) NOT NULL,

    -- 목표 유형 (체중 감량/유지/증량)
    goal_type VARCHAR(20) NOT NULL, -- lose_weight, maintain, gain_muscle

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
```

**BMR Calculation Reference (Mifflin-St Jeor Equation)**:
- Men: BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age + 5
- Women: BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age - 161

---

### 3. meals
사용자가 기록한 식단 내역

```sql
CREATE TABLE meals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,

    meal_type VARCHAR(20) NOT NULL, -- breakfast, lunch, dinner, snack
    food_name VARCHAR(255) NOT NULL,
    amount_g DECIMAL(10, 2) NOT NULL, -- 섭취량 (g)

    -- 영양소 정보
    calories INT NOT NULL,
    carbs_g DECIMAL(10, 2) NOT NULL,
    protein_g DECIMAL(10, 2) NOT NULL,
    fat_g DECIMAL(10, 2) NOT NULL,
    fiber_g DECIMAL(10, 2) DEFAULT 0,
    sugar_g DECIMAL(10, 2) DEFAULT 0,
    sodium_mg DECIMAL(10, 2) DEFAULT 0,

    consumed_at TIMESTAMP NOT NULL, -- 섭취 시간
    photo_url VARCHAR(500), -- 선택: 음식 사진
    notes TEXT, -- 메모

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_meals_user_id ON meals(user_id);
CREATE INDEX idx_meals_consumed_at ON meals(consumed_at);
CREATE INDEX idx_meals_user_consumed ON meals(user_id, consumed_at DESC);
```

---

### 4. nutrition_history
일별 영양소 섭취 집계 (리밸런싱 분석용)

```sql
CREATE TABLE nutrition_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,

    date DATE NOT NULL,

    -- 일일 총 섭취량
    total_calories INT NOT NULL,
    total_carbs_g DECIMAL(10, 2) NOT NULL,
    total_protein_g DECIMAL(10, 2) NOT NULL,
    total_fat_g DECIMAL(10, 2) NOT NULL,

    -- 목표 대비 차이 (잔여량, 음수면 초과)
    remaining_calories INT NOT NULL,
    remaining_carbs_g DECIMAL(10, 2) NOT NULL,
    remaining_protein_g DECIMAL(10, 2) NOT NULL,
    remaining_fat_g DECIMAL(10, 2) NOT NULL,

    -- 목표 달성률 (%)
    goal_achievement_pct DECIMAL(5, 2) NOT NULL,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(user_id, date)
);

CREATE INDEX idx_nutrition_history_user_date ON nutrition_history(user_id, date DESC);
```

**Note**: 이 테이블은 매일 자정에 배치 작업으로 업데이트되거나, 사용자가 식단을 기록할 때마다 실시간으로 갱신됩니다.

---

### 5. ingredients (Master Data)
식재료 영양소 데이터베이스

```sql
CREATE TABLE ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name VARCHAR(255) NOT NULL,
    name_en VARCHAR(255), -- 영문명
    category VARCHAR(50) NOT NULL, -- vegetable, protein, grain, dairy, fruit, etc.

    -- 100g 기준 영양소
    calories_per_100g INT NOT NULL,
    carbs_per_100g DECIMAL(10, 2) NOT NULL,
    protein_per_100g DECIMAL(10, 2) NOT NULL,
    fat_per_100g DECIMAL(10, 2) NOT NULL,
    fiber_per_100g DECIMAL(10, 2) DEFAULT 0,
    sugar_per_100g DECIMAL(10, 2) DEFAULT 0,
    sodium_per_100g DECIMAL(10, 2) DEFAULT 0,

    -- 외부 데이터 소스 참조
    usda_fdc_id VARCHAR(50), -- USDA FoodData Central ID

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_ingredients_name ON ingredients(name);
CREATE INDEX idx_ingredients_category ON ingredients(category);
CREATE UNIQUE INDEX idx_ingredients_usda ON ingredients(usda_fdc_id) WHERE usda_fdc_id IS NOT NULL;
```

**Data Source**: USDA FoodData Central API 또는 한국영양학회 데이터

---

### 6. inventory
사용자의 냉장고/식품 재고

```sql
CREATE TABLE inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    ingredient_id UUID REFERENCES ingredients(id) ON DELETE CASCADE,

    amount_g DECIMAL(10, 2) NOT NULL, -- 현재 보유량 (g)
    unit VARCHAR(20) NOT NULL, -- g, ml, piece, etc.

    purchase_date DATE,
    expiry_date DATE, -- 유통기한

    -- 재고 상태
    status VARCHAR(20) DEFAULT 'available', -- available, low_stock, expired
    low_stock_threshold DECIMAL(10, 2) DEFAULT 50, -- 재고 부족 알림 기준 (g)

    location VARCHAR(50), -- fridge, freezer, pantry
    notes TEXT,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_inventory_user_id ON inventory(user_id);
CREATE INDEX idx_inventory_expiry ON inventory(expiry_date);
CREATE INDEX idx_inventory_status ON inventory(status);
```

---

### 7. recipes
레시피 정보

```sql
CREATE TABLE recipes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name VARCHAR(255) NOT NULL,
    description TEXT,
    cuisine_type VARCHAR(50), -- korean, western, japanese, etc.

    -- 난이도 및 시간
    difficulty VARCHAR(20) NOT NULL, -- easy, medium, hard
    prep_time_minutes INT NOT NULL,
    cook_time_minutes INT NOT NULL,
    total_time_minutes INT GENERATED ALWAYS AS (prep_time_minutes + cook_time_minutes) STORED,

    servings INT NOT NULL DEFAULT 1, -- 기본 인분

    -- 조리법
    instructions TEXT NOT NULL, -- JSON 또는 TEXT (단계별 조리법)

    -- 레시피 총 영양소 (servings 기준)
    calories INT NOT NULL,
    carbs_g DECIMAL(10, 2) NOT NULL,
    protein_g DECIMAL(10, 2) NOT NULL,
    fat_g DECIMAL(10, 2) NOT NULL,

    -- AI 생성 여부
    is_ai_generated BOOLEAN DEFAULT FALSE,
    ai_prompt TEXT, -- Recipe Chef 에이전트가 사용한 프롬프트

    photo_url VARCHAR(500),
    tags TEXT[], -- [quick, high-protein, low-carb, vegetarian]

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_recipes_difficulty ON recipes(difficulty);
CREATE INDEX idx_recipes_total_time ON recipes(total_time_minutes);
CREATE INDEX idx_recipes_tags ON recipes USING GIN(tags);
```

---

### 8. recipe_ingredients
레시피와 재료 간의 Many-to-Many 관계

```sql
CREATE TABLE recipe_ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID REFERENCES recipes(id) ON DELETE CASCADE,
    ingredient_id UUID REFERENCES ingredients(id) ON DELETE CASCADE,

    amount_g DECIMAL(10, 2) NOT NULL, -- 필요량 (g)
    unit VARCHAR(20) NOT NULL, -- g, ml, piece, tsp, tbsp, etc.

    is_optional BOOLEAN DEFAULT FALSE, -- 선택 재료
    notes TEXT, -- "잘게 썰어주세요" 등

    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(recipe_id, ingredient_id)
);

CREATE INDEX idx_recipe_ingredients_recipe ON recipe_ingredients(recipe_id);
CREATE INDEX idx_recipe_ingredients_ingredient ON recipe_ingredients(ingredient_id);
```

---

## Agent Interaction Points

### Inventory Agent
- **Read**: `inventory`, `ingredients`
- **Trigger**: 유통기한 임박 시 알림 (expiry_date < NOW() + INTERVAL '3 days')
- **Update**: 레시피 조리 시 `inventory.amount_g` 차감

### Nutri-Strategist
- **Read**: `meals`, `nutrition_history`, `user_profiles`
- **Compute**: 일일 잔여 영양소, 이동 평균 편차 분석
- **Write**: `nutrition_history` 업데이트

### Recipe Chef
- **Read**: `nutrition_history` (잔여 영양소), `inventory` (가용 재료), `recipes`, `recipe_ingredients`
- **Compute**:
  - 잔여 영양소를 채울 수 있는 레시피 필터링
  - 재고 재료 매칭률 계산 (가용 재료 비율 > 80%)
- **Write**: 새로운 AI 생성 레시피 저장

---

## Sample Data Flow

### Example 1: 사용자가 아침 식사 기록
```sql
-- 1. 사용자가 "오트밀 50g + 바나나 100g" 기록
INSERT INTO meals (user_id, meal_type, food_name, amount_g, calories, carbs_g, protein_g, fat_g, consumed_at)
VALUES
  ('user-uuid', 'breakfast', 'Oatmeal', 50, 195, 34, 6.5, 3.5, '2026-02-05 08:00:00'),
  ('user-uuid', 'breakfast', 'Banana', 100, 89, 23, 1.1, 0.3, '2026-02-05 08:00:00');

-- 2. Nutri-Strategist가 nutrition_history 업데이트
UPDATE nutrition_history
SET
  total_calories = total_calories + 284,
  total_carbs_g = total_carbs_g + 57,
  total_protein_g = total_protein_g + 7.6,
  total_fat_g = total_fat_g + 3.8,
  remaining_calories = target_calories - (total_calories + 284),
  -- ... (다른 필드들도 동일하게 계산)
WHERE user_id = 'user-uuid' AND date = '2026-02-05';
```

### Example 2: Recipe Chef가 저녁 레시피 추천
```sql
-- 1. 잔여 영양소 조회
SELECT remaining_carbs_g, remaining_protein_g, remaining_fat_g
FROM nutrition_history
WHERE user_id = 'user-uuid' AND date = CURRENT_DATE;

-- 결과: carbs=80g, protein=60g, fat=20g

-- 2. 조건에 맞는 레시피 검색
SELECT r.id, r.name, r.carbs_g, r.protein_g, r.fat_g,
       COUNT(ri.ingredient_id) AS total_ingredients,
       COUNT(inv.ingredient_id) AS available_ingredients,
       (COUNT(inv.ingredient_id)::FLOAT / COUNT(ri.ingredient_id)) AS match_rate
FROM recipes r
JOIN recipe_ingredients ri ON r.id = ri.recipe_id
LEFT JOIN inventory inv ON ri.ingredient_id = inv.ingredient_id AND inv.user_id = 'user-uuid' AND inv.status = 'available'
WHERE r.carbs_g BETWEEN 70 AND 90
  AND r.protein_g BETWEEN 50 AND 70
  AND r.fat_g BETWEEN 15 AND 25
GROUP BY r.id
HAVING (COUNT(inv.ingredient_id)::FLOAT / COUNT(ri.ingredient_id)) >= 0.8
ORDER BY match_rate DESC, r.total_time_minutes ASC
LIMIT 3;
```

---

## Indexing Strategy

### High-Priority Indexes
1. `idx_meals_user_consumed` - 사용자별 식단 조회 (대시보드)
2. `idx_nutrition_history_user_date` - 일별 영양소 분석
3. `idx_inventory_user_id` + `idx_inventory_expiry` - 재고 조회 및 유통기한 알림
4. `idx_recipe_ingredients_recipe` - 레시피 상세 페이지

### Future Optimization
- Partitioning: `meals` 테이블을 월별로 파티셔닝 (데이터 누적 시)
- Materialized View: 주간/월간 영양소 트렌드 분석용

---

## Migration Strategy

### Phase 1: Core Schema
- users, user_profiles, meals, nutrition_history

### Phase 2: Recipe System
- ingredients, recipes, recipe_ingredients

### Phase 3: Inventory Management
- inventory

### Phase 4: Optimization
- Additional indexes, materialized views, triggers

---

**Last Updated**: 2026-02-05
**Version**: 1.0
