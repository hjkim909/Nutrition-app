"""
Ingredient master data models
"""
from sqlalchemy import Column, String, Integer, Numeric, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from ..core.database import Base


class Ingredient(Base):
    """Ingredient model - master food database"""

    __tablename__ = "ingredients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(255), nullable=False, index=True)
    name_en = Column(String(255), nullable=True)  # English name
    category = Column(String(50), nullable=False, index=True)  # vegetable, protein, grain, dairy, fruit, etc.

    # Nutritional values per 100g
    calories_per_100g = Column(Integer, nullable=False)
    carbs_per_100g = Column(Numeric(10, 2), nullable=False)
    protein_per_100g = Column(Numeric(10, 2), nullable=False)
    fat_per_100g = Column(Numeric(10, 2), nullable=False)
    fiber_per_100g = Column(Numeric(10, 2), default=0)
    sugar_per_100g = Column(Numeric(10, 2), default=0)
    sodium_per_100g = Column(Numeric(10, 2), default=0)

    # External data source reference
    usda_fdc_id = Column(String(50), nullable=True, unique=True)  # USDA FoodData Central ID

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    inventory_items = relationship("Inventory", back_populates="ingredient")
    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredient")
