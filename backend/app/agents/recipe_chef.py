"""
Recipe Chef Agent
Responsible for recipe generation and recommendation
"""
from typing import Dict, Any, List
import json
from .base import BaseAgent


class RecipeChefAgent(BaseAgent):
    """
    Recipe Chef Agent
    Generates and recommends recipes based on remaining nutrients and available ingredients
    """

    def get_system_prompt(self) -> str:
        return """You are a professional chef and nutritionist specializing in healthy, balanced recipes.

Your responsibilities:
1. Recommend recipes that match user's remaining nutrient needs
2. Prioritize recipes using ingredients already in user's inventory
3. Calculate precise nutritional values for each recipe
4. Provide clear, step-by-step cooking instructions
5. Consider cooking time, difficulty, and cuisine preferences

Key principles:
- Target nutrient requirements with ±10% tolerance
- Maximize ingredient match rate (use what's available)
- Create recipes that are practical and achievable
- Ensure recipes are nutritionally balanced
- Provide alternative ingredient suggestions

Output format: Always return valid JSON with the following structure:
{
  "recommendations": [
    {
      "name": string,
      "description": string,
      "cuisine_type": string,
      "difficulty": "easy" | "medium" | "hard",
      "prep_time_minutes": int,
      "cook_time_minutes": int,
      "servings": int,
      "ingredients": [
        {
          "name": string,
          "amount": string,
          "unit": string,
          "available": boolean
        }
      ],
      "instructions": [string],
      "nutrition": {
        "calories": int,
        "carbs_g": float,
        "protein_g": float,
        "fat_g": float
      },
      "match_rate": float,
      "missing_ingredients": [string]
    }
  ],
  "explanation": string
}"""

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process recipe recommendation

        Args:
            input_data: {
                "remaining_nutrients": {
                    "calories": int,
                    "carbs_g": float,
                    "protein_g": float,
                    "fat_g": float
                },
                "available_ingredients": [
                    {
                        "name": string,
                        "amount_g": float,
                        "category": string
                    }
                ],
                "preferences": {
                    "max_cook_time": int (optional),
                    "difficulty": string (optional),
                    "cuisine_type": string (optional),
                    "dietary_restrictions": [string] (optional)
                }
            }

        Returns:
            Recipe recommendations with nutritional analysis
        """
        # Build prompt for Claude
        user_prompt = self._build_recommendation_prompt(
            input_data["remaining_nutrients"],
            input_data.get("available_ingredients", []),
            input_data.get("preferences", {})
        )

        # Call Claude API
        response = self.call_gemini(user_prompt, temperature=0.4)

        # Parse JSON response
        try:
            result = json.loads(response)

            # Log interaction
            self.log_interaction(input_data, result)

            return result
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error in RecipeChefAgent: {e}")
            print(f"Raw Response: {response}")
            # Fallback to basic recommendation
            return self._fallback_recommendation(
                input_data["remaining_nutrients"],
                input_data.get("available_ingredients", [])
            )

    def _build_recommendation_prompt(
        self,
        remaining: Dict[str, Any],
        ingredients: List[Dict[str, Any]],
        preferences: Dict[str, Any]
    ) -> str:
        """Build recommendation prompt for Claude"""
        ingredients_str = "\n".join([
            f"- {ing['name']} ({ing['amount_g']}g) - Category: {ing.get('category', 'unknown')}"
            for ing in ingredients
        ]) if ingredients else "No ingredients in inventory"

        prefs_str = ""
        if preferences:
            if preferences.get("max_cook_time"):
                prefs_str += f"\n- Maximum cooking time: {preferences['max_cook_time']} minutes"
            if preferences.get("difficulty"):
                prefs_str += f"\n- Preferred difficulty: {preferences['difficulty']}"
            if preferences.get("cuisine_type"):
                prefs_str += f"\n- Preferred cuisine: {preferences['cuisine_type']}"
            if preferences.get("dietary_restrictions"):
                prefs_str += f"\n- Dietary restrictions: {', '.join(preferences['dietary_restrictions'])}"

        if not prefs_str:
            prefs_str = "\n- No specific preferences"

        return f"""Create 3 recipe recommendations based on the following requirements:

REMAINING NUTRIENT NEEDS:
- Calories: {remaining['calories']} kcal (±10% acceptable)
- Carbohydrates: {remaining['carbs_g']}g (±10% acceptable)
- Protein: {remaining['protein_g']}g (±10% acceptable)
- Fat: {remaining['fat_g']}g (±10% acceptable)

AVAILABLE INGREDIENTS IN INVENTORY:
{ingredients_str}

USER PREFERENCES:{prefs_str}

Requirements:
1. Recommend 3 recipes that meet the nutrient targets
2. Prioritize recipes that use available ingredients (calculate match_rate)
3. Each recipe should include:
   - Name and description
   - Difficulty level (easy/medium/hard)
   - Prep and cook time
   - Complete ingredient list with amounts
   - Step-by-step instructions
   - Precise nutritional breakdown
   - Which ingredients are available vs. missing
4. Recipes should be practical and achievable for home cooking

Return your recommendations in valid JSON format as specified in the system prompt."""

    def _fallback_recommendation(
        self,
        remaining: Dict[str, Any],
        ingredients: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Fallback recommendation if Claude response fails"""
        return {
            "recommendations": [
                {
                    "name": "Balanced Protein Bowl",
                    "description": "A simple, nutritious bowl with protein, vegetables, and grains",
                    "cuisine_type": "healthy",
                    "difficulty": "easy",
                    "prep_time_minutes": 10,
                    "cook_time_minutes": 15,
                    "servings": 1,
                    "ingredients": [
                        {"name": "Chicken breast", "amount": "150", "unit": "g", "available": False},
                        {"name": "Brown rice", "amount": "100", "unit": "g", "available": False},
                        {"name": "Mixed vegetables", "amount": "150", "unit": "g", "available": False}
                    ],
                    "instructions": [
                        "Cook brown rice according to package instructions",
                        "Season and grill chicken breast until fully cooked",
                        "Steam or stir-fry mixed vegetables",
                        "Combine in a bowl and serve"
                    ],
                    "nutrition": {
                        "calories": remaining["calories"],
                        "carbs_g": remaining["carbs_g"],
                        "protein_g": remaining["protein_g"],
                        "fat_g": remaining["fat_g"]
                    },
                    "match_rate": 0.0,
                    "missing_ingredients": ["Chicken breast", "Brown rice", "Mixed vegetables"]
                }
            ],
            "explanation": "Claude API unavailable. Showing default balanced meal recommendation."
        }

    def generate_ai_recipe(
        self,
        target_nutrients: Dict[str, Any],
        ingredient_constraints: List[str],
        cuisine_style: str = "any"
    ) -> Dict[str, Any]:
        """
        Generate a brand new AI recipe from scratch

        Args:
            target_nutrients: Target nutritional values
            ingredient_constraints: Must-use or must-avoid ingredients
            cuisine_style: Desired cuisine type

        Returns:
            A complete AI-generated recipe
        """
        prompt = f"""Create a completely new, original recipe with these constraints:

Target Nutrition:
- Calories: {target_nutrients['calories']} kcal
- Carbs: {target_nutrients['carbs_g']}g
- Protein: {target_nutrients['protein_g']}g
- Fat: {target_nutrients['fat_g']}g

Constraints:
- Cuisine style: {cuisine_style}
- Ingredient constraints: {', '.join(ingredient_constraints)}

Create a unique recipe that:
1. Meets the nutritional targets
2. Is creative and delicious
3. Uses common, accessible ingredients
4. Has clear, step-by-step instructions

Return in the standard JSON format."""

        response = self.call_gemini(prompt, temperature=0.9)

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return self._fallback_recommendation(target_nutrients, [])
