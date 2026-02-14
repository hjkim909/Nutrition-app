"""
Nutri-Strategist Agent
Responsible for nutrition analysis and rebalancing
"""
from typing import Dict, Any, List
from datetime import date
import json
from .base import BaseAgent


class NutriStrategistAgent(BaseAgent):
    """
    Nutri-Strategist Agent
    Analyzes user's daily nutrition intake and calculates remaining nutrients
    """

    def get_system_prompt(self) -> str:
        return """You are a professional nutritionist and data analyst specializing in personalized nutrition planning.

Your responsibilities:
1. Calculate total daily nutrient intake from meal records
2. Compare consumed nutrients against user's daily goals
3. Calculate remaining nutrients needed for the day
4. Identify nutritional imbalances (over/under consumption)
5. Provide actionable recommendations for the next meal

Key principles:
- Use precise calculations based on macronutrient ratios
- Consider BMR (Basal Metabolic Rate) and TDEE (Total Daily Energy Expenditure)
- Flag warnings when consumption deviates >20% from target
- Provide practical, achievable recommendations
- Focus on nutrient balance, not just calorie counting

Output format: Always return valid JSON with the following structure:
{
  "date": "YYYY-MM-DD",
  "consumed": {
    "calories": int,
    "carbs_g": float,
    "protein_g": float,
    "fat_g": float
  },
  "remaining": {
    "calories": int,
    "carbs_g": float,
    "protein_g": float,
    "fat_g": float
  },
  "goal_achievement_pct": float,
  "warnings": [string],
  "recommendations": string
}"""

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process nutrition analysis

        Args:
            input_data: {
                "user_id": str,
                "date": str (YYYY-MM-DD),
                "goals": {
                    "target_calories": int,
                    "target_carbs_g": float,
                    "target_protein_g": float,
                    "target_fat_g": float
                },
                "meals": [
                    {
                        "food_name": str,
                        "calories": int,
                        "carbs_g": float,
                        "protein_g": float,
                        "fat_g": float,
                        "meal_type": str,
                        "consumed_at": str
                    }
                ]
            }

        Returns:
            Nutrition balance analysis with remaining nutrients
        """
        # Calculate total consumed nutrients
        total_consumed = self._calculate_total_consumed(input_data["meals"])

        # Build prompt for Claude
        user_prompt = self._build_analysis_prompt(
            input_data["goals"],
            total_consumed,
            input_data["meals"]
        )

        # Call Claude API
        response = self.call_gemini(user_prompt, temperature=0.3)

        # Parse JSON response
        try:
            result = json.loads(response)
            result["date"] = input_data["date"]

            # Log interaction
            self.log_interaction(input_data, result)

            return result
        except json.JSONDecodeError:
            # Fallback to manual calculation if JSON parsing fails
            return self._fallback_calculation(
                input_data["goals"],
                total_consumed,
                input_data["date"]
            )

    def _calculate_total_consumed(self, meals: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate total nutrients from meals"""
        total = {
            "calories": 0,
            "carbs_g": 0.0,
            "protein_g": 0.0,
            "fat_g": 0.0,
        }

        for meal in meals:
            total["calories"] += meal.get("calories", 0)
            total["carbs_g"] += float(meal.get("carbs_g", 0))
            total["protein_g"] += float(meal.get("protein_g", 0))
            total["fat_g"] += float(meal.get("fat_g", 0))

        return total

    def _build_analysis_prompt(
        self,
        goals: Dict[str, Any],
        consumed: Dict[str, float],
        meals: List[Dict[str, Any]]
    ) -> str:
        """Build analysis prompt for Claude"""
        meals_str = "\n".join([
            f"- {meal['meal_type'].capitalize()}: {meal['food_name']} "
            f"({meal['calories']} kcal, C:{meal['carbs_g']}g, P:{meal['protein_g']}g, F:{meal['fat_g']}g)"
            for meal in meals
        ])

        return f"""Analyze the following daily nutrition data:

USER'S DAILY GOALS:
- Calories: {goals['target_calories']} kcal
- Carbohydrates: {goals['target_carbs_g']}g
- Protein: {goals['target_protein_g']}g
- Fat: {goals['target_fat_g']}g

MEALS CONSUMED TODAY:
{meals_str}

TOTAL CONSUMED:
- Calories: {consumed['calories']} kcal
- Carbohydrates: {consumed['carbs_g']}g
- Protein: {consumed['protein_g']}g
- Fat: {consumed['fat_g']}g

Please provide:
1. Remaining nutrients needed to meet daily goals
2. Goal achievement percentage
3. Warnings for any nutrient that's over/under by >20%
4. Specific recommendations for the next meal

Return your analysis in valid JSON format as specified in the system prompt."""

    def _fallback_calculation(
        self,
        goals: Dict[str, Any],
        consumed: Dict[str, float],
        date_str: str
    ) -> Dict[str, Any]:
        """Fallback calculation if Claude response fails"""
        remaining = {
            "calories": goals["target_calories"] - consumed["calories"],
            "carbs_g": float(goals["target_carbs_g"]) - consumed["carbs_g"],
            "protein_g": float(goals["target_protein_g"]) - consumed["protein_g"],
            "fat_g": float(goals["target_fat_g"]) - consumed["fat_g"],
        }

        goal_pct = (consumed["calories"] / goals["target_calories"]) * 100

        warnings = []
        if abs(goal_pct - 100) > 20:
            warnings.append(f"Total calorie intake is {abs(goal_pct - 100):.1f}% off target")

        return {
            "date": date_str,
            "consumed": consumed,
            "remaining": remaining,
            "goal_achievement_pct": round(goal_pct, 2),
            "warnings": warnings,
            "recommendations": "Continue balanced eating to meet your daily goals."
        }

    def calculate_bmr(
        self,
        weight_kg: float,
        height_cm: float,
        age: int,
        gender: str
    ) -> int:
        """
        Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation

        Args:
            weight_kg: Weight in kilograms
            height_cm: Height in centimeters
            age: Age in years
            gender: 'male' or 'female'

        Returns:
            BMR in kcal/day
        """
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age

        if gender.lower() == "male":
            bmr += 5
        elif gender.lower() == "female":
            bmr -= 161

        return int(bmr)

    def calculate_tdee(self, bmr: int, activity_level: str) -> int:
        """
        Calculate Total Daily Energy Expenditure

        Args:
            bmr: Basal Metabolic Rate
            activity_level: One of: sedentary, lightly_active, moderately_active, very_active

        Returns:
            TDEE in kcal/day
        """
        activity_multipliers = {
            "sedentary": 1.2,
            "lightly_active": 1.375,
            "moderately_active": 1.55,
            "very_active": 1.725,
        }

        multiplier = activity_multipliers.get(activity_level, 1.2)
        return int(bmr * multiplier)
