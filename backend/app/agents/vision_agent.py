from typing import Dict, Any, Optional
import json
import traceback

from .base import BaseAgent

class VisionAgent(BaseAgent):
    """Agent for analyzing food images to extract nutritional information."""

    def __init__(self, model: str = "gemini-3.1-flash-lite-preview"):
        # Use Gemini 3.1 Flash-Lite for cost-effective multimodal vision
        super().__init__(model=model)

    def get_system_prompt(self) -> str:
        return """You are an expert AI Nutritionist with advanced Computer Vision capabilities.
Your task is to analyze an image of food and extract precise nutritional information.

Analyze the image provided and return the result ONLY as a JSON object, with no markdown formatting and no extra text.
Do not wrap it in ```json blocks. 

The JSON object must strictly follow this exact schema:
{
  "food_name": "Recognized name of the food",
  "amount_g": Estimated total amount in grams (float),
  "calories": Estimated total calories (float),
  "carbs_g": Estimated total carbohydrates in grams (float),
  "protein_g": Estimated total protein in grams (float),
  "fat_g": Estimated total fat in grams (float),
  "confidence": Confidence score of your analysis between 0.0 and 1.0 (float),
  "description": "A brief 1-2 sentence description of the dish and your estimation logic"
}

If you cannot identify the food securely, provide your best guess, lower the confidence score, and state uncertainty in the description. Ensure the nutrition data is proportional to the estimated amount_g.
"""

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the image and return extracted nutritional info.

        Args:
            input_data: Must contain "image_base64" and "mime_type".
        
        Returns:
            Dict matching the VisionAnalyzeResponse schema.
        """
        image_base64 = input_data.get("image_base64", "")
        mime_type = input_data.get("mime_type", "image/jpeg")
        
        # Clean the base64 string if it contains the data prefix
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]

        system_prompt = self.get_system_prompt()
        
        image_part = {
            "mime_type": mime_type,
            "data": image_base64
        }
        
        user_message = "Please analyze this food image and provide the nutritional breakdown according to the requested JSON schema."
        
        try:
            # We bypass call_gemini because call_gemini only takes text user_message
            # We need to pass [system_prompt, user_message, image_part] directly to the model
            
            # Use specific generation config
            response = self.model.generate_content(
                [system_prompt, user_message, image_part],
                generation_config={
                    "temperature": 0.2, # Lower temperature for more consistent, factual estimations
                    "max_output_tokens": 1024,
                }
            )
            
            text = response.text
            
            # Clean up potential markdown code blocks
            if text.startswith("```"):
                lines = text.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip().startswith("```"):
                    lines = lines[:-1]
                text = "\n".join(lines).strip()
                
            return json.loads(text)

        except json.JSONDecodeError as e:
            print(f"Error decoding Vision AI response: {e}")
            print(f"Raw response: {text}")
            raise ValueError(f"AI response was not valid JSON. Response: {text}")
        except Exception as e:
            print(f"Error during Vision API call: {e}")
            traceback.print_exc()
            raise Exception(f"Vision AI analysis failed: {str(e)}")
