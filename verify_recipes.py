import requests
import json
import uuid
from datetime import datetime

BASE_URL = "http://localhost:8000"
# Use the same user ID as in seed_user.py
USER_ID = "550e8400-e29b-41d4-a716-446655440000"

def log(message, type="INFO"):
    print(f"[{type}] {message}")

def test_recipe_recommendation():
    url = f"{BASE_URL}/api/recipes/recommend"
    log("Testing Recipe Recommendation (this might take 10+ seconds)...", "INFO")
    
    payload = {
        "user_id": USER_ID,
        "date": datetime.now().date().isoformat(),
        "max_cook_time": 30,
        "difficulty": "medium",
        "cuisine_type": "healthy",
        "dietary_restrictions": []
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            if "recommendations" in data and len(data["recommendations"]) > 0:
                log(f"Recipe Recommendation passed. Received {len(data['recommendations'])} recipes.", "SUCCESS")
                print(json.dumps(data["recommendations"][0], indent=2, ensure_ascii=False))
                return data["recommendations"][0] # Return first recipe for detail test (if we had ID)
            else:
                log("Recipe Recommendation response empty or invalid", "WARNING")
                print(data)
                return None
        else:
            log(f"Recipe Recommendation failed: {response.status_code} - {response.text}", "ERROR")
            return None
    except Exception as e:
        log(f"Recipe Recommendation exception: {e}", "ERROR")
        return None

def main():
    log("Starting Recipe API Verification", "INFO")
    
    # 1. Test Recommendation
    recipe = test_recipe_recommendation()
    
    if recipe:
        log("Recipe details are part of recommendation response in this design.", "INFO")
        # Note: GET /recipes/{id} requires a real ID. 
        # Since recommendation doesn't save to DB automatically (it's just a suggestion), 
        # we can't test GET /{id} unless we modify the agent/service to save it 
        # OR we manually insert a recipe for testing.
        
        # For now, verification of POST /recommend is the main goal.

if __name__ == "__main__":
    main()
