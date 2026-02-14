"""Pydantic schemas for API requests and responses"""
from .users import (
    UserBase,
    UserCreate,
    UserResponse,
    UserProfileBase,
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
)
from .meals import (
    MealBase,
    MealCreate,
    MealUpdate,
    MealResponse,
    NutritionSummary,
    NutritionBalance,
)
from .recipes import (
    RecipeBase,
    RecipeCreate,
    RecipeUpdate,
    RecipeResponse,
    RecipeDetailResponse,
    RecipeRecommendationRequest,
    RecipeRecommendation,
    RecipeRecommendationResponse,
)
from .inventory import (
    InventoryBase,
    InventoryCreate,
    InventoryUpdate,
    InventoryResponse,
    InventoryAlert,
    InventoryAlertResponse,
)

__all__ = [
    # Users
    "UserBase",
    "UserCreate",
    "UserResponse",
    "UserProfileBase",
    "UserProfileCreate",
    "UserProfileUpdate",
    "UserProfileResponse",
    # Meals
    "MealBase",
    "MealCreate",
    "MealUpdate",
    "MealResponse",
    "NutritionSummary",
    "NutritionBalance",
    # Recipes
    "RecipeBase",
    "RecipeCreate",
    "RecipeUpdate",
    "RecipeResponse",
    "RecipeDetailResponse",
    "RecipeRecommendationRequest",
    "RecipeRecommendation",
    "RecipeRecommendationResponse",
    # Inventory
    "InventoryBase",
    "InventoryCreate",
    "InventoryUpdate",
    "InventoryResponse",
    "InventoryAlert",
    "InventoryAlertResponse",
]
