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
    def create_client(provider: str = None, model: str = None) -> LLMClient:
        """Create LLM client based on provider and model"""
        if not provider:
            provider = os.getenv('LLM_PROVIDER', 'ollama')
        
        if provider == 'ollama':
            from .ollama_client import OllamaClient
            model_name = model or os.getenv('LLM_MODEL', 'llama3.2:latest')
            return OllamaClient(model_name=model_name)
        elif provider == 'gemini':
            from .gemini_client import GeminiClient
            model_name = model or os.getenv('LLM_MODEL', 'gemini-1.5-flash')
            return GeminiClient(model_name=model_name)
        elif provider == 'deepseek':
            from .ollama_client import OllamaClient
            model_name = model or 'deepseek-r1:latest'
            return OllamaClient(model_name=model_name)
        elif provider == 'llama':
            from .ollama_client import OllamaClient
            model_name = model or 'llama3.2:latest'
            return OllamaClient(model_name=model_name)
        elif provider == 'openai':
            from .openai_client import OpenAIClient
            api_key = os.getenv('OPENAI_API_KEY')
            model_name = model or 'gpt-3.5-turbo'
            return OpenAIClient(api_key, model_name=model_name)
        elif provider == 'anthropic':
            from .anthropic_client import AnthropicClient
            api_key = os.getenv('ANTHROPIC_API_KEY')
            model_name = model or 'claude-3-haiku'
            return AnthropicClient(api_key, model_name=model_name)
        elif provider == 'huggingface':
            from .huggingface_client import HuggingFaceClient
            api_key = os.getenv('HUGGINGFACE_API_KEY')
            model_name = model or 'microsoft/DialoGPT-medium'
            return HuggingFaceClient(api_key, model_name=model_name)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}") 