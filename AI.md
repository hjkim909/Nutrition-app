# AI.md - Project Context & Status
> **Last Updated**: 2026-02-05
> **Current Phase**: Backend Development (Phase 4 completed, moving to Phase 4.2/5)

## 📌 Project Overview
**Name**: Nutrition (Nutri-Agent Flow)
**Type**: Full Stack Web App (AI-Integrated Nutrition Management)
**Tech Stack**:
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Google Gemini AI
- **Frontend**: Next.js (Planned), Tailwind CSS (Planned)
- **Infrastructure**: Docker for DB

## 🔄 Current Status
- **Backend**: ✅ Core API (Meals, Recipes) Operational
    - **Meals API**: CRUD + AI Analysis verified.
    - **Recipes API**: `POST /recommend` implemented (with AI fallback).
    - **Agents**: Nutri-Strategist (Verified), Recipe Chef (Implemented, tuning needed), Inventory Agent implemented.
    - **Database**: PostgreSQL linked via Docker. Schema fixed.
- **Frontend**: 🚧 Not started.

## 🛠 Recent Changes & Fixes
- **Recipes API**: Implemented `POST /api/recipes/recommend` and `GET /api/recipes/{id}`.
- **Agent Improvements**:
    - Fixed JSON parsing in `BaseAgent` (strip markdown).
    - Tuned `RecipeChefAgent` temperature (0.8 -> 0.4).
- **Database Schema**: Fixed `NoForeignKeysError` in `UserProfile` model.
- **AI Integration**: Switched Gemini model to `gemini-flash-latest`.
- **Verification**: 
    - Created `verify_api.py` and `verify_recipes.py`.
    - Verified Health Check, Meal CRUD, and AI Nutrition Analysis.

## 📝 Next Steps (ToDo)
1.  **Recipes API Implementation**:
    - Implement `POST /api/recipes/recommend` (connect to Recipe Chef Agent).
    - Implement `GET /api/recipes/{id}`.
2.  **Frontend Development**:
    - Initialize Next.js project structure (if not already robust).
    - Implement Dashboard and Meal Log UI.

## ℹ️ Key Information for Agents
- **Server**: Run with `uvicorn app.main:app --reload` (or VS Code debugger).
- **Tests**: Use `python verify_api.py` for quick backend verification.
- **User ID**: Test user UUID is `550e8400-e29b-41d4-a716-446655440000`.
- **Docs**: `claude.MD` contains detailed history of Phase 1-4.
