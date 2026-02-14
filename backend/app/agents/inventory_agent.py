"""
Inventory Agent
Responsible for inventory monitoring and alerts
"""
from typing import Dict, Any, List
from datetime import date, timedelta
import json
from .base import BaseAgent


class InventoryAgent(BaseAgent):
    """
    Inventory Agent
    Monitors user's fridge/pantry inventory and provides alerts
    """

    def get_system_prompt(self) -> str:
        return """You are a smart inventory management assistant specializing in food storage and meal planning.

Your responsibilities:
1. Monitor expiration dates and alert for items expiring soon
2. Track inventory levels and flag low stock items
3. Suggest purchase lists based on consumption patterns
4. Recommend meals to use up expiring ingredients
5. Provide food storage tips to extend shelf life

Key principles:
- Prioritize food safety (never recommend expired items)
- Reduce food waste by suggesting timely usage
- Consider user's eating patterns and preferences
- Provide practical, actionable recommendations
- Group alerts by urgency (immediate, soon, watch)

Output format: Always return valid JSON with the following structure:
{
  "urgent_alerts": [
    {
      "ingredient": string,
      "amount_g": float,
      "issue": "expiring" | "expired" | "low_stock",
      "days_until_expiry": int,
      "action": string
    }
  ],
  "upcoming_alerts": [
    {
      "ingredient": string,
      "amount_g": float,
      "issue": string,
      "days_until_expiry": int
    }
  ],
  "purchase_suggestions": [
    {
      "ingredient": string,
      "suggested_amount": string,
      "reason": string
    }
  ],
  "meal_suggestions": [
    {
      "ingredients_to_use": [string],
      "meal_idea": string,
      "urgency": "high" | "medium" | "low"
    }
  ],
  "storage_tips": [string]
}"""

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process inventory monitoring

        Args:
            input_data: {
                "user_id": str,
                "current_date": str (YYYY-MM-DD),
                "inventory": [
                    {
                        "ingredient_name": str,
                        "amount_g": float,
                        "expiry_date": str (YYYY-MM-DD) or null,
                        "low_stock_threshold": float,
                        "category": str,
                        "location": str (fridge/freezer/pantry)
                    }
                ],
                "recent_consumption": [
                    {
                        "ingredient_name": str,
                        "amount_used_g": float,
                        "date": str
                    }
                ] (optional)
            }

        Returns:
            Inventory alerts and recommendations
        """
        current_date = date.fromisoformat(input_data["current_date"])

        # Analyze inventory for issues
        urgent_alerts, upcoming_alerts = self._analyze_inventory(
            input_data["inventory"],
            current_date
        )

        # Build prompt for Claude
        user_prompt = self._build_monitoring_prompt(
            input_data["inventory"],
            urgent_alerts,
            upcoming_alerts,
            input_data.get("recent_consumption", [])
        )

        # Call Claude API
        response = self.call_gemini(user_prompt, temperature=0.5)

        # Parse JSON response
        try:
            result = json.loads(response)

            # Ensure urgent and upcoming alerts are included
            result["urgent_alerts"] = urgent_alerts
            result["upcoming_alerts"] = upcoming_alerts

            # Log interaction
            self.log_interaction(input_data, result)

            return result
        except json.JSONDecodeError:
            # Fallback to basic alert
            return self._fallback_monitoring(urgent_alerts, upcoming_alerts)

    def _analyze_inventory(
        self,
        inventory: List[Dict[str, Any]],
        current_date: date
    ) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Analyze inventory for urgent and upcoming issues"""
        urgent_alerts = []
        upcoming_alerts = []

        for item in inventory:
            # Check expiration
            if item.get("expiry_date"):
                expiry = date.fromisoformat(item["expiry_date"])
                days_until_expiry = (expiry - current_date).days

                if days_until_expiry < 0:
                    urgent_alerts.append({
                        "ingredient": item["ingredient_name"],
                        "amount_g": item["amount_g"],
                        "issue": "expired",
                        "days_until_expiry": days_until_expiry,
                        "action": f"DISCARD IMMEDIATELY - Expired {abs(days_until_expiry)} days ago"
                    })
                elif days_until_expiry <= 2:
                    urgent_alerts.append({
                        "ingredient": item["ingredient_name"],
                        "amount_g": item["amount_g"],
                        "issue": "expiring",
                        "days_until_expiry": days_until_expiry,
                        "action": f"USE TODAY - Expires in {days_until_expiry} day(s)"
                    })
                elif days_until_expiry <= 7:
                    upcoming_alerts.append({
                        "ingredient": item["ingredient_name"],
                        "amount_g": item["amount_g"],
                        "issue": "expiring_soon",
                        "days_until_expiry": days_until_expiry
                    })

            # Check low stock
            if item["amount_g"] < item.get("low_stock_threshold", 50):
                alert = {
                    "ingredient": item["ingredient_name"],
                    "amount_g": item["amount_g"],
                    "issue": "low_stock",
                    "threshold": item.get("low_stock_threshold", 50)
                }

                if item["amount_g"] == 0:
                    alert["action"] = "OUT OF STOCK - Restock immediately"
                    urgent_alerts.append(alert)
                else:
                    alert["action"] = f"Running low - Only {item['amount_g']}g remaining"
                    upcoming_alerts.append(alert)

        return urgent_alerts, upcoming_alerts

    def _build_monitoring_prompt(
        self,
        inventory: List[Dict[str, Any]],
        urgent_alerts: List[Dict[str, Any]],
        upcoming_alerts: List[Dict[str, Any]],
        recent_consumption: List[Dict[str, Any]]
    ) -> str:
        """Build monitoring prompt for Claude"""
        inventory_str = "\n".join([
            f"- {item['ingredient_name']}: {item['amount_g']}g "
            f"(Expires: {item.get('expiry_date', 'N/A')}, Location: {item.get('location', 'unknown')})"
            for item in inventory
        ])

        urgent_str = "\n".join([
            f"- {alert['ingredient']}: {alert['action']}"
            for alert in urgent_alerts
        ]) if urgent_alerts else "None"

        upcoming_str = "\n".join([
            f"- {alert['ingredient']}: {alert['issue']} ({alert.get('days_until_expiry', 'N/A')} days)"
            for alert in upcoming_alerts
        ]) if upcoming_alerts else "None"

        consumption_str = "\n".join([
            f"- {item['ingredient_name']}: {item['amount_used_g']}g on {item['date']}"
            for item in recent_consumption[-10:]  # Last 10 items
        ]) if recent_consumption else "No recent consumption data"

        return f"""Analyze this user's inventory and provide intelligent recommendations:

CURRENT INVENTORY:
{inventory_str}

URGENT ALERTS (Expired or Expiring Within 2 Days):
{urgent_str}

UPCOMING ALERTS (Low Stock or Expiring Within 7 Days):
{upcoming_str}

RECENT CONSUMPTION PATTERNS:
{consumption_str}

Please provide:
1. Purchase suggestions based on:
   - Items that are out of stock or low
   - Items frequently used (from consumption patterns)
   - Items needed to complete common meal combinations
2. Meal suggestions that:
   - Use ingredients expiring soon (prioritize urgent items)
   - Are practical and achievable
   - Match the ingredient categories available
3. Storage tips for:
   - Items that are at risk of spoiling
   - How to extend shelf life
   - Proper storage locations (fridge/freezer/pantry)

Return your analysis in valid JSON format as specified in the system prompt."""

    def _fallback_monitoring(
        self,
        urgent_alerts: List[Dict[str, Any]],
        upcoming_alerts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Fallback monitoring if Claude response fails"""
        purchase_suggestions = []
        meal_suggestions = []

        # Basic purchase suggestions for low stock items
        for alert in urgent_alerts + upcoming_alerts:
            if alert.get("issue") == "low_stock":
                purchase_suggestions.append({
                    "ingredient": alert["ingredient"],
                    "suggested_amount": "500g",
                    "reason": "Currently low in stock"
                })

        # Basic meal suggestions for expiring items
        expiring_items = [
            alert["ingredient"]
            for alert in urgent_alerts
            if alert.get("issue") in ["expired", "expiring"]
        ]

        if expiring_items:
            meal_suggestions.append({
                "ingredients_to_use": expiring_items[:3],
                "meal_idea": f"Use {', '.join(expiring_items[:3])} in a stir-fry or soup",
                "urgency": "high"
            })

        return {
            "urgent_alerts": urgent_alerts,
            "upcoming_alerts": upcoming_alerts,
            "purchase_suggestions": purchase_suggestions,
            "meal_suggestions": meal_suggestions,
            "storage_tips": [
                "Store perishables in airtight containers",
                "Keep refrigerator at 40°F (4°C) or below",
                "Use FIFO method: First In, First Out"
            ]
        }

    def estimate_shelf_life(
        self,
        ingredient_category: str,
        storage_location: str
    ) -> int:
        """
        Estimate shelf life in days based on category and storage

        Args:
            ingredient_category: Category of ingredient (vegetable, protein, dairy, etc.)
            storage_location: Where it's stored (fridge, freezer, pantry)

        Returns:
            Estimated shelf life in days
        """
        shelf_life_map = {
            ("vegetable", "fridge"): 7,
            ("vegetable", "freezer"): 180,
            ("vegetable", "pantry"): 3,
            ("protein", "fridge"): 3,
            ("protein", "freezer"): 180,
            ("fruit", "fridge"): 7,
            ("fruit", "freezer"): 180,
            ("fruit", "pantry"): 5,
            ("dairy", "fridge"): 7,
            ("dairy", "freezer"): 90,
            ("grain", "pantry"): 365,
            ("grain", "fridge"): 180,
        }

        return shelf_life_map.get(
            (ingredient_category.lower(), storage_location.lower()),
            30  # Default 30 days
        )
