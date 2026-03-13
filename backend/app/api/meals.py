"""
Meals API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from uuid import UUID

from ..core.database import get_db
from ..schemas.meals import (
    MealCreate,
    MealUpdate,
    MealResponse,
    NutritionBalance
)
from ..schemas.vision import VisionAnalyzeRequest, VisionAnalyzeResponse
from ..services.meals_service import MealsService
from ..agents.vision_agent import VisionAgent

router = APIRouter()


@router.post("/", response_model=MealResponse, status_code=201)
def create_meal(
    meal: MealCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new meal record

    - **user_id**: User ID
    - **meal_type**: breakfast, lunch, dinner, or snack
    - **food_name**: Name of the food
    - **amount_g**: Amount in grams
    - **calories**: Calorie content
    - **carbs_g, protein_g, fat_g**: Macronutrients in grams
    """
    service = MealsService(db)
    return service.create_meal(meal)


@router.get("/", response_model=List[MealResponse])
def get_meals(
    user_id: UUID,
    date_from: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    meal_type: Optional[str] = Query(None, description="Filter by meal type"),
    db: Session = Depends(get_db)
):
    """
    Get meals with optional filters

    - **user_id**: User ID (required)
    - **date_from**: Start date for filtering
    - **date_to**: End date for filtering
    - **meal_type**: Filter by meal type (breakfast, lunch, dinner, snack)
    """
    service = MealsService(db)
    return service.get_meals(user_id, date_from, date_to, meal_type)


@router.get("/{meal_id}", response_model=MealResponse)
def get_meal(
    meal_id: UUID,
    user_id: UUID = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Get a single meal by ID"""
    service = MealsService(db)
    meal = service.get_meal_by_id(meal_id, user_id)

    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    return meal


@router.put("/{meal_id}", response_model=MealResponse)
def update_meal(
    meal_id: UUID,
    meal_data: MealUpdate,
    user_id: UUID = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Update a meal record"""
    service = MealsService(db)
    meal = service.update_meal(meal_id, user_id, meal_data)

    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    return meal


@router.delete("/{meal_id}", status_code=204)
def delete_meal(
    meal_id: UUID,
    user_id: UUID = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Delete a meal record"""
    service = MealsService(db)
    success = service.delete_meal(meal_id, user_id)

    if not success:
        raise HTTPException(status_code=404, detail="Meal not found")

    return None


@router.get("/nutrition/balance", response_model=NutritionBalance)
def get_nutrition_balance(
    user_id: UUID,
    date_param: Optional[date] = Query(None, alias="date", description="Date (YYYY-MM-DD), defaults to today"),
    db: Session = Depends(get_db)
):
    """
    Get nutrition balance for a specific date using Nutri-Strategist AI agent

    Returns consumed vs remaining nutrients, goal achievement, warnings, and recommendations
    """
    service = MealsService(db)
    target_date = date_param or date.today()

    try:
        balance = service.get_nutrition_balance(user_id, target_date)
        return balance
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating nutrition balance: {str(e)}")


@router.post("/analyze-image", response_model=VisionAnalyzeResponse)
def analyze_meal_image(request: VisionAnalyzeRequest):
    """
    Analyze a food image using Vision AI (Gemini 3.1 Flash-Lite) to extract nutritional info.
    
    Expects a base64 encoded image string.
    Returns estimated food name, calories, macros, and confidence score.
    """
    agent = VisionAgent()
    try:
        input_data = {
            "image_base64": request.image_base64,
            "mime_type": request.mime_type
        }
        result = agent.process(input_data)
        return VisionAnalyzeResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vision analysis failed: {str(e)}")

