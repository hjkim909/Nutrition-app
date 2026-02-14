"""
User schemas for API requests and responses
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """Schema for creating a new user"""
    pass


class UserResponse(UserBase):
    """Schema for user response"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserProfileBase(BaseModel):
    """Base user profile schema"""
    age: int = Field(..., ge=10, le=120)
    gender: str = Field(..., pattern="^(male|female)$")
    height_cm: float = Field(..., ge=50, le=300)
    weight_kg: float = Field(..., ge=20, le=500)
    activity_level: str = Field(
        ...,
        pattern="^(sedentary|lightly_active|moderately_active|very_active)$"
    )
    goal_type: str = Field(
        ...,
        pattern="^(lose_weight|maintain|gain_muscle)$"
    )


class UserProfileCreate(UserProfileBase):
    """Schema for creating user profile"""
    user_id: UUID


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile"""
    age: Optional[int] = Field(None, ge=10, le=120)
    gender: Optional[str] = Field(None, pattern="^(male|female)$")
    height_cm: Optional[float] = Field(None, ge=50, le=300)
    weight_kg: Optional[float] = Field(None, ge=20, le=500)
    activity_level: Optional[str] = None
    goal_type: Optional[str] = None


class UserProfileResponse(UserProfileBase):
    """Schema for user profile response"""
    id: UUID
    user_id: UUID
    bmr_kcal: int
    tdee_kcal: int
    target_calories: int
    target_carbs_g: float
    target_protein_g: float
    target_fat_g: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
