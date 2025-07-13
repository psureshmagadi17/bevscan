import os
import json
from typing import Dict, Any
from .client import LLMClient
from .ollama_client import OllamaClient

class HuggingFaceClient(LLMClient):
    """HuggingFace client for LLM processing (fallback to Ollama)"""
    
    def __init__(self, api_key: str = None, model_name: str = "microsoft/DialoGPT-medium"):
        self.api_key = api_key
        self.model_name = model_name
        
        # For now, always use Ollama as fallback since HuggingFace setup is complex
        print("⚠️  HuggingFace client not yet implemented, using Ollama")
        self.ollama_client = OllamaClient(model_name="llama3.2")
        self.use_ollama = True
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from prompt"""
        if self.use_ollama:
            return self.ollama_client.generate(prompt, **kwargs)
        else:
            raise NotImplementedError("HuggingFace client not yet implemented")
    
    def generate_structured(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured response following schema"""
        if self.use_ollama:
            return self.ollama_client.generate_structured(prompt, schema)
        else:
            raise NotImplementedError("HuggingFace client not yet implemented") 