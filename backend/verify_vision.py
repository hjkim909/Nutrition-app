import asyncio
import base64
from app.agents.vision_agent import VisionAgent

def create_dummy_image_base64() -> str:
    # 1x1 red pixel JPEG base64
    return "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA="


def test_vision():
    print("Initializing VisionAgent...")
    agent = VisionAgent()
    
    print("Creating dummy image...")
    img_base64 = create_dummy_image_base64()
    
    input_data = {
        "image_base64": img_base64,
        "mime_type": "image/jpeg"
    }
    
    print("Calling Gemini Vision AI...")
    try:
        result = agent.process(input_data)
        print("Success! Result:")
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_vision()
