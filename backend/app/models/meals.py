"""
Meal tracking models
"""
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Text, func, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from ..core.database import Base


class Meal(Base):
    """Meal model - user's food intake records"""

    __tablename__ = "meals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    meal_type = Column(String(20), nullable=False)  # breakfast, lunch, dinner, snack
    food_name = Column(String(255), nullable=False)
    amount_g = Column(Numeric(10, 2), nullable=False)  # Amount in grams

    # Nutritional information
    calories = Column(Integer, nullable=False)
    carbs_g = Column(Numeric(10, 2), nullable=False)
    protein_g = Column(Numeric(10, 2), nullable=False)
    fat_g = Column(Numeric(10, 2), nullable=False)
    fiber_g = Column(Numeric(10, 2), default=0)
    sugar_g = Column(Numeric(10, 2), default=0)
    sodium_mg = Column(Numeric(10, 2), default=0)

    consumed_at = Column(DateTime(timezone=True), nullable=False, index=True)
    photo_url = Column(String(500), nullable=True)  # Optional photo
    notes = Column(Text, nullable=True)  # User notes

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="meals")


class NutritionHistory(Base):
    """Daily nutrition aggregate (for rebalancing analysis)"""

    __tablename__ = "nutrition_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    date = Column(Date, nullable=False)

    # Daily total intake
    total_calories = Column(Integer, nullable=False)
    total_carbs_g = Column(Numeric(10, 2), nullable=False)
    total_protein_g = Column(Numeric(10, 2), nullable=False)
    total_fat_g = Column(Numeric(10, 2), nullable=False)

    # Remaining vs goal (negative means exceeded)
    remaining_calories = Column(Integer, nullable=False)
    remaining_carbs_g = Column(Numeric(10, 2), nullable=False)
    remaining_protein_g = Column(Numeric(10, 2), nullable=False)
    remaining_fat_g = Column(Numeric(10, 2), nullable=False)

    # Goal achievement percentage
    goal_achievement_pct = Column(Numeric(5, 2), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="nutrition_history")

    __table_args__ = (
        {"schema": None},
    )
