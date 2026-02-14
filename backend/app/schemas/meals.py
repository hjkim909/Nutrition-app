"""
Meal schemas for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class MealBase(BaseModel):
    """Base meal schema"""
    meal_type: str = Field(..., pattern="^(breakfast|lunch|dinner|snack)$")
    food_name: str = Field(..., min_length=1, max_length=255)
    amount_g: float = Field(..., ge=0)
    calories: int = Field(..., ge=0)
    carbs_g: float = Field(..., ge=0)
    protein_g: float = Field(..., ge=0)
    fat_g: float = Field(..., ge=0)
    fiber_g: Optional[float] = Field(default=0, ge=0)
    sugar_g: Optional[float] = Field(default=0, ge=0)
    sodium_mg: Optional[float] = Field(default=0, ge=0)
    notes: Optional[str] = None


class MealCreate(MealBase):
    """Schema for creating a meal record"""
    user_id: UUID
    consumed_at: datetime
    photo_url: Optional[str] = None


class MealUpdate(BaseModel):
    """Schema for updating a meal record"""
    meal_type: Optional[str] = Field(None, pattern="^(breakfast|lunch|dinner|snack)$")
    food_name: Optional[str] = Field(None, min_length=1, max_length=255)
    amount_g: Optional[float] = Field(None, ge=0)
    calories: Optional[int] = Field(None, ge=0)
    carbs_g: Optional[float] = Field(None, ge=0)
    protein_g: Optional[float] = Field(None, ge=0)
    fat_g: Optional[float] = Field(None, ge=0)
    fiber_g: Optional[float] = Field(None, ge=0)
    sugar_g: Optional[float] = Field(None, ge=0)
    sodium_mg: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None
    photo_url: Optional[str] = None


class MealResponse(MealBase):
    """Schema for meal response"""
    id: UUID
    user_id: UUID
    consumed_at: datetime
    photo_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class NutritionSummary(BaseModel):
    """Daily nutrition summary"""
    date: str
    total_calories: int
    total_carbs_g: float
    total_protein_g: float
    total_fat_g: float
    meal_count: int


class NutritionBalance(BaseModel):
    """Nutrition balance response from Nutri-Strategist agent"""
    date: str
    consumed: dict
    remaining: dict
    goal_achievement_pct: float
    warnings: list[str]
    recommendations: str
