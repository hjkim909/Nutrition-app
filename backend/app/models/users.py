"""
User models
"""
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Boolean, Date, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from ..core.database import Base


class User(Base):
    """User model - basic user information"""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")
    nutrition_history = relationship("NutritionHistory", back_populates="user", cascade="all, delete-orphan")
    inventory = relationship("Inventory", back_populates="user", cascade="all, delete-orphan")


class UserProfile(Base):
    """User profile - physical information and nutrition goals"""

    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)

    # Physical information (for BMR calculation)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)  # male, female
    height_cm = Column(Numeric(5, 2), nullable=False)
    weight_kg = Column(Numeric(5, 2), nullable=False)
    activity_level = Column(String(20), nullable=False)  # sedentary, lightly_active, moderately_active, very_active

    # Calculated BMR and goals
    bmr_kcal = Column(Integer, nullable=False)  # Basal Metabolic Rate
    tdee_kcal = Column(Integer, nullable=False)  # Total Daily Energy Expenditure

    # Daily nutrition goals (g)
    target_calories = Column(Integer, nullable=False)
    target_carbs_g = Column(Numeric(10, 2), nullable=False)
    target_protein_g = Column(Numeric(10, 2), nullable=False)
    target_fat_g = Column(Numeric(10, 2), nullable=False)

    # Goal type (weight loss/maintenance/muscle gain)
    goal_type = Column(String(20), nullable=False)  # lose_weight, maintain, gain_muscle

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")
