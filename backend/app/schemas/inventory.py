"""
Inventory schemas for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID


class InventoryBase(BaseModel):
    """Base inventory schema"""
    ingredient_id: UUID
    amount_g: float = Field(..., ge=0)
    unit: str = Field(..., min_length=1, max_length=20)
    purchase_date: Optional[date] = None
    expiry_date: Optional[date] = None
    status: str = Field(default="available", pattern="^(available|low_stock|expired)$")
    low_stock_threshold: float = Field(default=50, ge=0)
    location: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None


class InventoryCreate(InventoryBase):
    """Schema for creating inventory item"""
    user_id: UUID


class InventoryUpdate(BaseModel):
    """Schema for updating inventory item"""
    amount_g: Optional[float] = Field(None, ge=0)
    unit: Optional[str] = Field(None, min_length=1, max_length=20)
    purchase_date: Optional[date] = None
    expiry_date: Optional[date] = None
    status: Optional[str] = Field(None, pattern="^(available|low_stock|expired)$")
    low_stock_threshold: Optional[float] = Field(None, ge=0)
    location: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None


class InventoryResponse(InventoryBase):
    """Schema for inventory response"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InventoryAlert(BaseModel):
    """Single inventory alert"""
    ingredient: str
    amount_g: float
    issue: str
    days_until_expiry: Optional[int] = None
    action: Optional[str] = None


class PurchaseSuggestion(BaseModel):
    """Purchase suggestion"""
    ingredient: str
    suggested_amount: str
    reason: str


class MealSuggestion(BaseModel):
    """Meal suggestion to use expiring ingredients"""
    ingredients_to_use: List[str]
    meal_idea: str
    urgency: str


class InventoryAlertResponse(BaseModel):
    """Response from Inventory Agent"""
    urgent_alerts: List[InventoryAlert]
    upcoming_alerts: List[InventoryAlert]
    purchase_suggestions: List[PurchaseSuggestion]
    meal_suggestions: List[MealSuggestion]
    storage_tips: List[str]
