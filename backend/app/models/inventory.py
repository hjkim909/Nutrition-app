"""
Inventory management models
"""
from sqlalchemy import Column, String, Numeric, DateTime, Date, Text, Boolean, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from ..core.database import Base


class Inventory(Base):
    """Inventory model - user's fridge/pantry stock"""

    __tablename__ = "inventory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    ingredient_id = Column(UUID(as_uuid=True), ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False)

    amount_g = Column(Numeric(10, 2), nullable=False)  # Current stock in grams
    unit = Column(String(20), nullable=False)  # g, ml, piece, etc.

    purchase_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True, index=True)  # Expiration date

    # Inventory status
    status = Column(String(20), default="available")  # available, low_stock, expired
    low_stock_threshold = Column(Numeric(10, 2), default=50)  # Low stock alert threshold (g)

    location = Column(String(50), nullable=True)  # fridge, freezer, pantry
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="inventory")
    ingredient = relationship("Ingredient", back_populates="inventory_items")
