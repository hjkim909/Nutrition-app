"""
Recipe schemas for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class RecipeIngredientBase(BaseModel):
    """Base recipe ingredient schema"""
    ingredient_id: UUID
    amount_g: float = Field(..., ge=0)
    unit: str = Field(..., min_length=1, max_length=20)
    is_optional: bool = False
    notes: Optional[str] = None


class RecipeIngredientCreate(RecipeIngredientBase):
    """Schema for creating recipe ingredient"""
    pass


class RecipeIngredientResponse(RecipeIngredientBase):
    """Schema for recipe ingredient response"""
    id: UUID
    recipe_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class RecipeBase(BaseModel):
    """Base recipe schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$")
    prep_time_minutes: int = Field(..., ge=0)
    cook_time_minutes: int = Field(..., ge=0)
    servings: int = Field(default=1, ge=1)
    instructions: str
    calories: int = Field(..., ge=0)
    carbs_g: float = Field(..., ge=0)
    protein_g: float = Field(..., ge=0)
    fat_g: float = Field(..., ge=0)
    photo_url: Optional[str] = None
    tags: Optional[List[str]] = None


class RecipeCreate(RecipeBase):
    """Schema for creating a recipe"""
    ingredients: List[RecipeIngredientCreate]
    is_ai_generated: bool = False
    ai_prompt: Optional[str] = None


class RecipeUpdate(BaseModel):
    """Schema for updating a recipe"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    difficulty: Optional[str] = Field(None, pattern="^(easy|medium|hard)$")
    prep_time_minutes: Optional[int] = Field(None, ge=0)
    cook_time_minutes: Optional[int] = Field(None, ge=0)
    servings: Optional[int] = Field(None, ge=1)
    instructions: Optional[str] = None
    calories: Optional[int] = Field(None, ge=0)
    carbs_g: Optional[float] = Field(None, ge=0)
    protein_g: Optional[float] = Field(None, ge=0)
    fat_g: Optional[float] = Field(None, ge=0)
    photo_url: Optional[str] = None
    tags: Optional[List[str]] = None


class RecipeResponse(RecipeBase):
    """Schema for recipe response"""
    id: UUID
    is_ai_generated: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RecipeDetailResponse(RecipeResponse):
    """Schema for recipe detail with ingredients"""
    ingredients: List[RecipeIngredientResponse]


class RecipeRecommendationRequest(BaseModel):
    """Schema for recipe recommendation request"""
    user_id: UUID
    date: Optional[str] = None  # YYYY-MM-DD, defaults to today
    max_cook_time: Optional[int] = Field(None, ge=0)
    difficulty: Optional[str] = Field(None, pattern="^(easy|medium|hard)$")
    cuisine_type: Optional[str] = None
    dietary_restrictions: Optional[List[str]] = None


class RecipeRecommendation(BaseModel):
    """Single recipe recommendation from Recipe Chef agent"""
    name: str
    description: str
    cuisine_type: str
    difficulty: str
    prep_time_minutes: int
    cook_time_minutes: int
    servings: int
    ingredients: List[dict]
    instructions: List[str]
    nutrition: dict
    match_rate: float
    missing_ingredients: List[str]


class RecipeRecommendationResponse(BaseModel):
    """Response from Recipe Chef agent"""
    recommendations: List[RecipeRecommendation]
    explanation: str
