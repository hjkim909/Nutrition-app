import sys
import os
import uuid
from dotenv import load_dotenv

# Load .env from backend directory
load_dotenv(os.path.join(os.getcwd(), "backend", ".env"))

# Add backend directory to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.core.database import SessionLocal
from app.models.users import User, UserProfile

def seed():
    db = SessionLocal()
    user_id = uuid.UUID("550e8400-e29b-41d4-a716-446655440000")
    
    try:
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            print(f"User {user_id} already exists.")
            return

        print("Creating user...")
        new_user = User(
            id=user_id,
            email="test@example.com",
            name="Test User"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print("Creating profile...")
        new_profile = UserProfile(
            user_id=user_id,
            age=30,
            gender="male",
            height_cm=175.0,
            weight_kg=70.0,
            activity_level="moderately_active",
            bmr_kcal=1700,
            tdee_kcal=2500,
            target_calories=2000,
            target_carbs_g=250.0,
            target_protein_g=150.0,
            target_fat_g=44.0,
            goal_type="maintain"
        )
        db.add(new_profile)
        db.commit()
        print("User and profile created successfully.")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
