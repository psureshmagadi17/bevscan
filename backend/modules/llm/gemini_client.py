import os
import json
from typing import Dict, Any
import google.generativeai as genai
from .client import LLMClient

class GeminiClient(LLMClient):
    """Google Gemini client for LLM processing"""
    
    def __init__(self, api_key: str = None, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from prompt"""
        try:
            response = self.model.generate_content(prompt, **kwargs)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {e}")
    
    def generate_structured(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured response following schema"""
        # Create structured prompt with JSON schema
        structured_prompt = f"""
{prompt}

Please respond with valid JSON following this exact schema:
{json.dumps(schema, indent=2)}

Important: Respond only with the JSON object, no additional text or explanations.
"""
        
        response_text = self.generate(structured_prompt)
        
        # Try to extract JSON from response
        try:
            # Find JSON in response (sometimes models add extra text)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON response: {e}")
    
    def generate_with_safety_settings(self, prompt: str, safety_settings: list = None) -> str:
        """Generate response with custom safety settings"""
        if safety_settings:
            model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)
        else:
            model = self.model
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {e}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about available models"""
        try:
            models = genai.list_models()
            return {
                "models": [model.name for model in models if 'generateContent' in model.supported_generation_methods],
                "current_model": self.model.model_name
            }
        except Exception as e:
            raise Exception(f"Failed to get model info: {e}") 