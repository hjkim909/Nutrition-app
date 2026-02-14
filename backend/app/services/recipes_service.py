from sqlalchemy.orm import Session, joinedload
from typing import List, Optional, Dict, Any
from datetime import date
from uuid import UUID

from ..models import Recipe, RecipeIngredient, Inventory, Ingredient
from ..schemas.recipes import RecipeCreate, RecipeUpdate
from ..agents import RecipeChefAgent
from .meals_service import MealsService

class RecipesService:
    def __init__(self, db: Session):
        self.db = db
        self.meals_service = MealsService(db)
        self.chef_agent = RecipeChefAgent()

    def get_recommendations(self, user_id: UUID, date: date, preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get recipe recommendations based on remaining nutrients and inventory
        """
        # 1. Get remaining nutrients from MealsService
        # We handle the case where user might not have a profile yet gracefully in MealsService
        try:
            nutrition_balance = self.meals_service.get_nutrition_balance(user_id, date)
            remaining = nutrition_balance.get("remaining", {})
        except Exception as e:
            # Fallback if nutrition balance calculation fails (e.g. no profile)
            print(f"Error calculating nutrition balance: {e}")
            remaining = {
                "calories": 600,
                "carbs_g": 60.0,
                "protein_g": 30.0,
                "fat_g": 20.0
            }

        # 2. Get available ingredients from Inventory
        # Use joinedload to fetch associated Ingredient data efficiently
        inventory_items = self.db.query(Inventory).options(
            joinedload(Inventory.ingredient)
        ).filter(
            Inventory.user_id == user_id,
            Inventory.status == "available"
        ).all()

        available_ingredients = []
        for item in inventory_items:
            if item.ingredient:
                available_ingredients.append({
                    "name": item.ingredient.name,
                    "amount_g": float(item.amount_g),
                    "category": item.ingredient.category
                })

        # 3. Call RecipeChefAgent
        input_data = {
            "remaining_nutrients": remaining,
            "available_ingredients": available_ingredients,
            "preferences": preferences or {}
        }
        
        return self.chef_agent.process(input_data)

    def get_recipe(self, recipe_id: UUID) -> Optional[Recipe]:
        """
        Get a recipe by ID with ingredients
        """
        return self.db.query(Recipe).options(
            joinedload(Recipe.recipe_ingredients).joinedload(RecipeIngredient.ingredient)
        ).filter(Recipe.id == recipe_id).first()
