from fastapi import APIRouter, Depends, Query, HTTPException, Path
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date
from typing import List, Optional

from ..core.database import get_db
from ..schemas.recipes import RecipeResponse, RecipeDetailResponse, RecipeRecommendationResponse, RecipeRecommendationRequest
from ..services.recipes_service import RecipesService

router = APIRouter()

@router.post("/recommend", response_model=RecipeRecommendationResponse)
async def recommend_recipes(
    request: RecipeRecommendationRequest,
    db: Session = Depends(get_db)
):
    """
    Get AI-powered recipe recommendations based on user's nutrition status and inventory
    """
    service = RecipesService(db)
    try:
        recommendations = service.get_recommendations(
            user_id=request.user_id,
            date=date.today(),  # Uses today for remaining nutrient calculation
            preferences={
                "max_cook_time": request.max_cook_time,
                "difficulty": request.difficulty,
                "cuisine_type": request.cuisine_type,
                "dietary_restrictions": request.dietary_restrictions
            }
        )
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{recipe_id}", response_model=RecipeDetailResponse)
async def get_recipe(
    recipe_id: UUID = Path(..., title="The ID of the recipe to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Get a specific recipe by ID with ingredients
    """
    service = RecipesService(db)
    recipe = service.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
