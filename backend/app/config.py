from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost/bevscan"
    
    # LLM Configuration
    LLM_PROVIDER: str = "ollama"  # Options: ollama, gemini, openai, anthropic, huggingface
    LLM_MODEL: str = "llama3.1:8b"  # Model name for the selected provider
    
    # API Keys (only required for cloud providers)
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".pdf", ".png", ".jpg", ".jpeg", ".tiff"]
    
    # Security
    JWT_SECRET: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Processing
    OCR_CONFIDENCE_THRESHOLD: float = 0.7
    LLM_CONFIDENCE_THRESHOLD: float = 0.8
    PRICE_CHANGE_THRESHOLD: float = 0.05  # 5%
    
    class Config:
        env_file = "../.env"
        case_sensitive = True

# Global settings instance
settings = Settings()

# LLM Provider Configuration
LLM_CONFIGS = {
    "ollama": {
        "name": "Ollama (Local)",
        "free": True,
        "setup_required": True,
        "setup_instructions": "Install Ollama: curl -fsSL https://ollama.ai/install.sh | sh",
        "models": ["llama3.1:8b", "mistral:7b", "codellama:7b"],
        "recommended_model": "llama3.1:8b"
    },
    "gemini": {
        "name": "Google Gemini",
        "free": True,
        "setup_required": False,
        "api_key_required": True,
        "models": ["gemini-pro", "gemini-pro-vision"],
        "recommended_model": "gemini-pro"
    },
    "openai": {
        "name": "OpenAI GPT",
        "free": False,
        "setup_required": False,
        "api_key_required": True,
        "free_tier": "$5/month credit",
        "models": ["gpt-3.5-turbo", "gpt-4"],
        "recommended_model": "gpt-3.5-turbo"
    },
    "anthropic": {
        "name": "Anthropic Claude",
        "free": False,
        "setup_required": False,
        "api_key_required": True,
        "free_tier": "$5/month credit",
        "models": ["claude-3-haiku", "claude-3-sonnet"],
        "recommended_model": "claude-3-haiku"
    },
    "huggingface": {
        "name": "Hugging Face",
        "free": True,
        "setup_required": False,
        "api_key_required": False,
        "models": ["microsoft/DialoGPT-medium", "gpt2"],
        "recommended_model": "microsoft/DialoGPT-medium"
    }
} 