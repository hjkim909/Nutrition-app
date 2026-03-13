# AI.md - Project Context & Status
> **Last Updated**: 2026-03-07
> **Current Phase**: Phase 5 (Frontend Development) & Phase 4.2 (Vision AI Integration)

## 📌 Project Overview
**Name**: Nutrition (Nutri-Agent Flow)
**Type**: Full Stack Web App (AI-Integrated Nutrition Management)
**Tech Stack**:
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Google Gemini AI
- **Frontend**: Next.js (Planned), Tailwind CSS (Planned)
- **Infrastructure**: Docker for DB
- **Repository**: [GitHub](https://github.com/hjkim909/Nutrition-app)

## 🔄 Current Status
- **Backend**: ✅ Core API (Meals, Recipes) Operational
    - **Meals API**: CRUD + AI Analysis verified.
    - **Recipes API**: `POST /recommend` implemented (with AI fallback).
    - **Agents**: Nutri-Strategist (Verified), Recipe Chef (Implemented, tuning needed), Inventory Agent implemented.
    - **Database**: PostgreSQL linked via Docker. Schema fixed.
- **Frontend**: ✅ Dashboard and Vision Log Operational (Phase 5)
    - Next.js App Router, Tailwind CSS, Recharts, Shadcn UI integrated.
    - Connected to Backend API (`/api/meals` and `/api/meals/nutrition/balance`).
    - Camera/gallery upload via Gemini 3.1 Flash-Lite AI integrated.
## 🛠 Recent Changes & Fixes
- **Vision AI Migration (Phase 4.2)**: 
    - Added `POST /api/meals/analyze-image` using `gemini-3.1-flash-lite-preview` for robust and cost-effective image recognition.
    - Verified JSON schema structure parsing with `verify_vision.py`.
- **Frontend Dashboard (Phase 5)**:
    - Initialized Next.js, Tailwind, Recharts, and Shadcn UI.
    - Built Main Dashboard (`app/page.tsx`) with charts and nutrition progress.
    - Built Vision Log UI (`app/meals/page.tsx`) with Camera & Gallery uploads.
- **Recipes API**: Implemented `POST /api/recipes/recommend` and `GET /api/recipes/{id}`.
    - Tuned `RecipeChefAgent` temperature (0.8 -> 0.4).
- **Database Schema**: Fixed `NoForeignKeysError` in `UserProfile` model.
- **AI Integration**: Switched Gemini model to `gemini-flash-latest` (Prior). Now migrating vision/multimodal features to `gemini-3.1-flash-lite` for cost-efficiency.
- **Verification**: 
    - Created `verify_api.py` and `verify_recipes.py`.
    - Verified Health Check, Meal CRUD, and AI Nutrition Analysis.

## 📝 Next Steps (ToDo)
1.  **Recipes UI (Phase 6)**:
    - Build UI to display AI recommendations from the `RecipeChefAgent`.
    - Integrate `POST /api/recipes/recommend` to the frontend.
2.  **Inventory UI (Phase 7)**:
    - Build UI to track fridge items and integrate with the `Inventory Agent`.
## ℹ️ Key Information for Agents
- **Server**: Run with `uvicorn app.main:app --reload` (or VS Code debugger).
- **Tests**: Use `python verify_api.py` for quick backend verification.
- **User ID**: Test user UUID is `550e8400-e29b-41d4-a716-446655440000`.
- **Docs**: `claude.MD` contains detailed history of Phase 1-4.
