from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import os

class LLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from prompt"""
        pass
    
    @abstractmethod
    def generate_structured(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured response following schema"""
        pass

class LLMFactory:
    """Factory for creating LLM clients"""
    
    @staticmethod
    def create_client(provider: str = None) -> LLMClient:
        """Create LLM client based on provider"""
        if not provider:
            provider = os.getenv('LLM_PROVIDER', 'ollama')
        
        if provider == 'ollama':
            from .ollama_client import OllamaClient
            return OllamaClient()
        elif provider == 'gemini':
            from .gemini_client import GeminiClient
            return GeminiClient()
        elif provider == 'openai':
            from .openai_client import OpenAIClient
            api_key = os.getenv('OPENAI_API_KEY')
            return OpenAIClient(api_key)
        elif provider == 'anthropic':
            from .anthropic_client import AnthropicClient
            api_key = os.getenv('ANTHROPIC_API_KEY')
            return AnthropicClient(api_key)
        elif provider == 'huggingface':
            from .huggingface_client import HuggingFaceClient
            api_key = os.getenv('HUGGINGFACE_API_KEY')
            return HuggingFaceClient(api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}") 