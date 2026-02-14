import requests
import json
import uuid
from datetime import datetime

BASE_URL = "http://localhost:8000"
USER_ID = "550e8400-e29b-41d4-a716-446655440000"

def log(message, type="INFO"):
    print(f"[{type}] {message}")

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            log("Health check passed", "SUCCESS")
            return True
        else:
            log(f"Health check failed: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"Health check exception: {e}", "ERROR")
        return False

def test_create_meal():
    url = f"{BASE_URL}/api/meals"
    meal_data = {
        "user_id": USER_ID,
        "meal_type": "breakfast",
        "food_name": "Test Oatmeal",
        "amount_g": 150,
        "calories": 284,
        "carbs_g": 57,
        "protein_g": 7.6,
        "fat_g": 3.8,
        "consumed_at": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(url, json=meal_data)
        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            log(f"Create meal passed: ID {data.get('id')}", "SUCCESS")
            return data.get('id')
        else:
            log(f"Create meal failed: {response.status_code} - {response.text}", "ERROR")
            return None
    except Exception as e:
        log(f"Create meal exception: {e}", "ERROR")
        return None

def test_get_meals(meal_id):
    url = f"{BASE_URL}/api/meals?user_id={USER_ID}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            meals = response.json()
            found = any(m['id'] == meal_id for m in meals)
            if found:
                log(f"Get meals passed (Found {meal_id})", "SUCCESS")
                return True
            else:
                log("Get meals failed (Created meal not found)", "ERROR")
                return False
        else:
            log(f"Get meals failed: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"Get meals exception: {e}", "ERROR")
        return False

def test_ai_analysis():
    url = f"{BASE_URL}/api/meals/nutrition/balance?user_id={USER_ID}"
    log("Testing AI Analysis (this might take a few seconds)...", "INFO")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "consumed" in data or "remaining" in data or "recommendations" in data:
                log("AI Analysis passed", "SUCCESS")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                return True
            else:
                log("AI Analysis response unexpected format", "WARNING")
                return False
        else:
            log(f"AI Analysis failed: {response.status_code} - {response.text}", "ERROR")
            return False
    except Exception as e:
        log(f"AI Analysis exception: {e}", "ERROR")
        return False

def main():
    log("Starting API Verification", "INFO")
    
    if not test_health():
        return
    
    meal_id = test_create_meal()
    if not meal_id:
        return
        
    if not test_get_meals(meal_id):
        pass # Continue anyway
        
    test_ai_analysis()

if __name__ == "__main__":
    main()
