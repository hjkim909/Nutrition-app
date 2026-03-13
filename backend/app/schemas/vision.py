from typing import Optional
from pydantic import BaseModel, Field

class VisionAnalyzeRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded image string (with or without data:image/jpeg;base64, prefix)")
    mime_type: str = Field(default="image/jpeg", description="MIME type of the image (e.g., image/jpeg, image/png)")

class VisionAnalyzeResponse(BaseModel):
    food_name: str = Field(..., description="Recognized name of the food")
    amount_g: float = Field(..., description="Estimated amount in grams")
    calories: float = Field(..., description="Estimated total calories")
    carbs_g: float = Field(..., description="Estimated total carbohydrates in grams")
    protein_g: float = Field(..., description="Estimated total protein in grams")
    fat_g: float = Field(..., description="Estimated total fat in grams")
    confidence: float = Field(default=0.0, description="Confidence score of the analysis (0.0 to 1.0)")
    description: Optional[str] = Field(default=None, description="Brief description or notes from AI")
