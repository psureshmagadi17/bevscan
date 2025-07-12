import requests
import json
from typing import Dict, Any
from .client import LLMClient

class OllamaClient(LLMClient):
    """Ollama client for local LLM processing"""
    
    def __init__(self, model_name: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = model_name
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from prompt"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    **kwargs
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama API error: {e}")
    
    def generate_structured(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured response following schema"""
        # Add schema instructions to prompt
        structured_prompt = f"""
{prompt}

Please respond with valid JSON following this schema:
{json.dumps(schema, indent=2)}

Response:
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
    
    def list_models(self) -> list:
        """List available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return response.json()["models"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to list models: {e}")
    
    def pull_model(self, model_name: str) -> bool:
        """Pull a model from Ollama registry"""
        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name}
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to pull model: {e}") 