"""
Base Agent class for all AI agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import google.generativeai as genai
from ..core.config import get_settings

settings = get_settings()

# Configure Gemini API
genai.configure(api_key=settings.gemini_api_key)


class BaseAgent(ABC):
    """Base class for all AI agents"""

    def __init__(self, model: str = "gemini-flash-latest"):
        """
        Initialize the base agent

        Args:
            model: Gemini model to use (default: Gemini Flash Latest)
                  Options: gemini-flash-latest, gemini-pro, gemini-1.5-flash
        """
        self.model_name = model
        self.model = genai.GenerativeModel(
            model_name=model,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 4096,
            }
        )
        self.max_tokens = 4096

    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Get the system prompt for this agent
        Must be implemented by subclasses
        """
        pass

    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input data and return results
        Must be implemented by subclasses

        Args:
            input_data: Input data specific to this agent

        Returns:
            Processed results as a dictionary
        """
        pass

    def call_gemini(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """
        Call Gemini API with the given message

        Args:
            user_message: The user's message/prompt
            system_prompt: Optional system prompt (uses get_system_prompt if not provided)
            temperature: Sampling temperature (0-1)

        Returns:
            Gemini's response as a string
        """
        if system_prompt is None:
            system_prompt = self.get_system_prompt()

        # Combine system prompt and user message for Gemini
        full_prompt = f"{system_prompt}\n\n---\n\nUser Request:\n{user_message}"

        # Update generation config with custom temperature
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": self.max_tokens,
        }

        model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=generation_config
        )

        response = model.generate_content(full_prompt)
        
        text = response.text
        
        # Clean up markdown code blocks if present
        if text.startswith("```"):
            # Remove first line (```json or ```)
            text = "\n".join(text.split("\n")[1:])
            # Remove last line (```)
            if text.strip().endswith("```"):
                text = text.strip()[:-3]
        
        return text.strip()

    def log_interaction(self, input_data: Dict[str, Any], output_data: Dict[str, Any]):
        """
        Log agent interactions for debugging and analysis

        Args:
            input_data: Input that was provided to the agent
            output_data: Output that was returned by the agent
        """
        # TODO: Implement logging to agent_interaction.log
        pass
