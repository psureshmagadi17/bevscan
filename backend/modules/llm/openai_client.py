import os
import json
from typing import Dict, Any
from .client import LLMClient
from .ollama_client import OllamaClient

class OpenAIClient(LLMClient):
    """OpenAI client for LLM processing (fallback to Ollama if no API key)"""
    
    def __init__(self, api_key: str = None, model_name: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model_name = model_name
        
        # If no API key, fallback to Ollama
        if not self.api_key:
            print("⚠️  No OpenAI API key provided, falling back to Ollama")
            self.ollama_client = OllamaClient(model_name="llama3.2")
            self.use_ollama = True
        else:
            self.use_ollama = False
            # TODO: Implement actual OpenAI client when API key is available
            raise NotImplementedError("OpenAI client not yet implemented. Please use Ollama or Gemini for now.")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from prompt"""
        if self.use_ollama:
            return self.ollama_client.generate(prompt, **kwargs)
        else:
            raise NotImplementedError("OpenAI client not yet implemented")
    
    def generate_structured(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured response following schema"""
        if self.use_ollama:
            return self.ollama_client.generate_structured(prompt, schema)
        else:
            raise NotImplementedError("OpenAI client not yet implemented") 