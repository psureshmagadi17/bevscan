import os
import json
from typing import Dict, Any
from .client import LLMClient
from .ollama_client import OllamaClient

class AnthropicClient(LLMClient):
    """Anthropic client for LLM processing (fallback to Ollama if no API key)"""
    
    def __init__(self, api_key: str = None, model_name: str = "claude-3-haiku"):
        self.api_key = api_key
        self.model_name = model_name
        
        # If no API key, fallback to Ollama
        if not self.api_key:
            print("⚠️  No Anthropic API key provided, falling back to Ollama")
            self.ollama_client = OllamaClient(model_name="llama3.2")
            self.use_ollama = True
        else:
            self.use_ollama = False
            # TODO: Implement actual Anthropic client when API key is available
            raise NotImplementedError("Anthropic client not yet implemented. Please use Ollama or Gemini for now.")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from prompt"""
        if self.use_ollama:
            return self.ollama_client.generate(prompt, **kwargs)
        else:
            raise NotImplementedError("Anthropic client not yet implemented")
    
    def generate_structured(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured response following schema"""
        if self.use_ollama:
            return self.ollama_client.generate_structured(prompt, schema)
        else:
            raise NotImplementedError("Anthropic client not yet implemented") 