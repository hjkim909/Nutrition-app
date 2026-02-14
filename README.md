# Nutri-Agent Flow

AI 기반 영양 관리 및 식단 추천 풀스택 애플리케이션

## Project Structure

```
Nutrition/
├── backend/          # FastAPI Backend
│   ├── app/
│   │   ├── main.py           # FastAPI application entry
│   │   ├── api/              # API endpoints (routes)
│   │   ├── models/           # SQLAlchemy ORM models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── agents/           # AI agent implementations
│   │   ├── services/         # Business logic layer
│   │   └── core/             # Config, database, dependencies
│   ├── alembic/              # Database migrations
│   │   └── versions/         # Migration files
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Environment variables template
│
├── frontend/         # Next.js Frontend
│   ├── app/                  # Next.js App Router pages
│   ├── components/
│   │   ├── ui/               # Shadcn UI components
│   │   └── features/         # Feature-specific components
│   ├── lib/                  # Utilities and helpers
│   ├── public/               # Static assets
│   ├── package.json
│   └── .env.example
│
├── PRD.md                    # Product Requirements Document
├── DATABASE_SCHEMA.md        # Database schema and ERD
└── README.md                 # This file
```

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **AI**: Anthropic Claude API (for agent orchestration)
- **MCP**: Model Context Protocol for data integration

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **UI Library**: Shadcn UI
- **Styling**: Tailwind CSS 3.4+
- **State**: React Context / Zustand
- **Forms**: React Hook Form + Zod

## Features

### Core Capabilities
1. **Meal Logging** - 식단 기록 및 영양소 자동 계산
2. **Nutrient Rebalancing** - 실시간 잔여 영양소 계산 (Nutri-Strategist Agent)
3. **Recipe Recommendation** - 잔여 영양소 기반 레시피 추천 (Recipe Chef Agent)
4. **Inventory Management** - 냉장고 재고 추적 및 유통기한 알림 (Inventory Agent)

### AI Agents
- **Nutri-Strategist**: BMR 기반 영양소 리밸런싱 및 분석
- **Recipe Chef**: 가용 재료와 잔여 영양소 기반 레시피 생성
- **Inventory Agent**: 재고 모니터링 및 구매 추천

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Anthropic API Key

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the server:
```bash
uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your configuration
```

4. Start development server:
```bash
npm run dev
```

App will be available at `http://localhost:3000`

## API Endpoints

### Meals
- `POST /api/meals` - Create meal record
- `GET /api/meals` - Get user's meals
- `PUT /api/meals/{id}` - Update meal
- `DELETE /api/meals/{id}` - Delete meal

### Nutrition
- `GET /api/nutrition/balance` - Get daily nutrient balance
- `POST /api/nutrition/goals` - Set nutrition goals

### Recipes
- `POST /api/recipes/recommend` - Get recipe recommendations
- `GET /api/recipes/{id}` - Get recipe details
- `POST /api/recipes/{id}/add-to-meal` - Add recipe to meal plan

### Inventory
- `GET /api/inventory` - Get user's inventory
- `POST /api/inventory` - Add ingredient to inventory
- `PUT /api/inventory/{id}` - Update inventory item
- `DELETE /api/inventory/{id}` - Remove from inventory

## Development Workflow

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Deployment

### Backend (Render/Railway)
- Set environment variables
- Deploy from Git repository
- Run migrations automatically

### Frontend (Vercel)
- Connect GitHub repository
- Set environment variables
- Automatic deployments on push

## Contributing

This is a private project developed with AI assistance (Claude Code).

## License

Private - All Rights Reserved

---

**Version**: 1.0
**Last Updated**: 2026-02-05
