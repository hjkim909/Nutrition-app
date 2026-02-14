"""
Meals service - Business logic for meal operations
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from uuid import UUID

from ..models import Meal, NutritionHistory, UserProfile
from ..schemas.meals import MealCreate, MealUpdate
from ..agents import NutriStrategistAgent


class MealsService:
    """Service for meal-related operations"""

    def __init__(self, db: Session):
        self.db = db
        self.nutri_agent = NutriStrategistAgent()

    def create_meal(self, meal_data: MealCreate) -> Meal:
        """Create a new meal record"""
        meal = Meal(**meal_data.model_dump())
        self.db.add(meal)
        self.db.commit()
        self.db.refresh(meal)

        # Update nutrition history
        self._update_nutrition_history(meal.user_id, meal.consumed_at.date())

        return meal

    def get_meals(
        self,
        user_id: UUID,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        meal_type: Optional[str] = None
    ) -> List[Meal]:
        """Get meals with optional filters"""
        query = self.db.query(Meal).filter(Meal.user_id == user_id)

        if date_from:
            query = query.filter(Meal.consumed_at >= date_from)
        if date_to:
            query = query.filter(Meal.consumed_at <= date_to)
        if meal_type:
            query = query.filter(Meal.meal_type == meal_type)

        return query.order_by(Meal.consumed_at.desc()).all()

    def get_meal_by_id(self, meal_id: UUID, user_id: UUID) -> Optional[Meal]:
        """Get a meal by ID"""
        return self.db.query(Meal).filter(
            Meal.id == meal_id,
            Meal.user_id == user_id
        ).first()

    def update_meal(self, meal_id: UUID, user_id: UUID, meal_data: MealUpdate) -> Optional[Meal]:
        """Update a meal record"""
        meal = self.get_meal_by_id(meal_id, user_id)
        if not meal:
            return None

        update_data = meal_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(meal, key, value)

        self.db.commit()
        self.db.refresh(meal)

        # Update nutrition history
        self._update_nutrition_history(meal.user_id, meal.consumed_at.date())

        return meal

    def delete_meal(self, meal_id: UUID, user_id: UUID) -> bool:
        """Delete a meal record"""
        meal = self.get_meal_by_id(meal_id, user_id)
        if not meal:
            return False

        consumed_date = meal.consumed_at.date()
        self.db.delete(meal)
        self.db.commit()

        # Update nutrition history
        self._update_nutrition_history(user_id, consumed_date)

        return True

    def _update_nutrition_history(self, user_id: UUID, target_date: date):
        """Update or create nutrition history for a specific date"""
        # Get all meals for the date
        meals = self.db.query(Meal).filter(
            Meal.user_id == user_id,
            Meal.consumed_at >= datetime.combine(target_date, datetime.min.time()),
            Meal.consumed_at < datetime.combine(target_date, datetime.max.time())
        ).all()

        # Calculate totals
        total_calories = sum(meal.calories for meal in meals)
        total_carbs = sum(float(meal.carbs_g) for meal in meals)
        total_protein = sum(float(meal.protein_g) for meal in meals)
        total_fat = sum(float(meal.fat_g) for meal in meals)

        # Get user's goals
        profile = self.db.query(UserProfile).filter(
            UserProfile.user_id == user_id
        ).first()

        if not profile:
            return  # No profile, skip history update

        # Calculate remaining
        remaining_calories = profile.target_calories - total_calories
        remaining_carbs = float(profile.target_carbs_g) - total_carbs
        remaining_protein = float(profile.target_protein_g) - total_protein
        remaining_fat = float(profile.target_fat_g) - total_fat

        # Calculate goal achievement percentage
        goal_pct = (total_calories / profile.target_calories * 100) if profile.target_calories > 0 else 0

        # Update or create history
        history = self.db.query(NutritionHistory).filter(
            NutritionHistory.user_id == user_id,
            NutritionHistory.date == target_date
        ).first()

        if history:
            history.total_calories = total_calories
            history.total_carbs_g = total_carbs
            history.total_protein_g = total_protein
            history.total_fat_g = total_fat
            history.remaining_calories = remaining_calories
            history.remaining_carbs_g = remaining_carbs
            history.remaining_protein_g = remaining_protein
            history.remaining_fat_g = remaining_fat
            history.goal_achievement_pct = goal_pct
        else:
            history = NutritionHistory(
                user_id=user_id,
                date=target_date,
                total_calories=total_calories,
                total_carbs_g=total_carbs,
                total_protein_g=total_protein,
                total_fat_g=total_fat,
                remaining_calories=remaining_calories,
                remaining_carbs_g=remaining_carbs,
                remaining_protein_g=remaining_protein,
                remaining_fat_g=remaining_fat,
                goal_achievement_pct=goal_pct
            )
            self.db.add(history)

        self.db.commit()

    def get_nutrition_balance(self, user_id: UUID, target_date: date) -> dict:
        """Get nutrition balance using Nutri-Strategist agent"""
        # Get user profile
        profile = self.db.query(UserProfile).filter(
            UserProfile.user_id == user_id
        ).first()

        if not profile:
            raise ValueError("User profile not found")

        # Get meals for the date
        meals = self.db.query(Meal).filter(
            Meal.user_id == user_id,
            Meal.consumed_at >= datetime.combine(target_date, datetime.min.time()),
            Meal.consumed_at < datetime.combine(target_date, datetime.max.time())
        ).all()

        # Prepare data for agent
        meals_data = [{
            "food_name": meal.food_name,
            "calories": meal.calories,
            "carbs_g": float(meal.carbs_g),
            "protein_g": float(meal.protein_g),
            "fat_g": float(meal.fat_g),
            "meal_type": meal.meal_type,
            "consumed_at": meal.consumed_at.isoformat()
        } for meal in meals]

        goals = {
            "target_calories": profile.target_calories,
            "target_carbs_g": float(profile.target_carbs_g),
            "target_protein_g": float(profile.target_protein_g),
            "target_fat_g": float(profile.target_fat_g)
        }

        # Call Nutri-Strategist agent
        result = self.nutri_agent.process({
            "user_id": str(user_id),
            "date": target_date.isoformat(),
            "goals": goals,
            "meals": meals_data
        })

        return result
