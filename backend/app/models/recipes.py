"""
Recipe models
"""
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Text, Boolean, ForeignKey, func, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from ..core.database import Base


class Recipe(Base):
    """Recipe model - cooking recipes"""

    __tablename__ = "recipes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    cuisine_type = Column(String(50), nullable=True)  # korean, western, japanese, etc.

    # Difficulty and time
    difficulty = Column(String(20), nullable=False, index=True)  # easy, medium, hard
    prep_time_minutes = Column(Integer, nullable=False)
    cook_time_minutes = Column(Integer, nullable=False)
    # total_time_minutes is auto-calculated in PostgreSQL

    servings = Column(Integer, nullable=False, default=1)  # Number of servings

    # Cooking instructions
    instructions = Column(Text, nullable=False)  # JSON or TEXT (step-by-step)

    # Total recipe nutrition (for servings)
    calories = Column(Integer, nullable=False)
    carbs_g = Column(Numeric(10, 2), nullable=False)
    protein_g = Column(Numeric(10, 2), nullable=False)
    fat_g = Column(Numeric(10, 2), nullable=False)

    # AI generation
    is_ai_generated = Column(Boolean, default=False)
    ai_prompt = Column(Text, nullable=True)  # Prompt used by Recipe Chef agent

    photo_url = Column(String(500), nullable=True)
    tags = Column(ARRAY(String), nullable=True)  # [quick, high-protein, low-carb, vegetarian]

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    recipe_ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")


class RecipeIngredient(Base):
    """Recipe-Ingredient relationship (Many-to-Many)"""

    __tablename__ = "recipe_ingredients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False, index=True)
    ingredient_id = Column(UUID(as_uuid=True), ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False, index=True)

    amount_g = Column(Numeric(10, 2), nullable=False)  # Required amount (g)
    unit = Column(String(20), nullable=False)  # g, ml, piece, tsp, tbsp, etc.

    is_optional = Column(Boolean, default=False)  # Optional ingredient
    notes = Column(Text, nullable=True)  # "Finely chopped", etc.

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    recipe = relationship("Recipe", back_populates="recipe_ingredients")
    ingredient = relationship("Ingredient", back_populates="recipe_ingredients")
