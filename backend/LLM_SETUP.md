# LLM Provider Setup Guide

This guide helps you set up different LLM providers for BevScan.

## 🏆 **Recommended: Ollama (Local & Free)**

### Setup Instructions
```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Start Ollama service
ollama serve

# 3. Pull a model (in another terminal)
ollama pull llama3.1:8b

# 4. Test the model
ollama run llama3.1:8b "Hello, how are you?"
```

### Environment Configuration
```bash
# .env file
LLM_PROVIDER=ollama
LLM_MODEL=llama3.1:8b
OLLAMA_BASE_URL=http://localhost:11434
```

### Available Models
- `llama3.1:8b` - Best balance of speed and quality
- `mistral:7b` - Fast and efficient
- `codellama:7b` - Good for structured data
- `llama3.1:70b` - Highest quality (requires more RAM)

### Pros
- ✅ Completely free
- ✅ No API rate limits
- ✅ Privacy-first (data stays local)
- ✅ No internet required after setup
- ✅ Multiple model options

### Cons
- ❌ Requires local installation
- ❌ Needs sufficient RAM (8GB+ recommended)
- ❌ Initial model download (2-4GB per model)

---

## 🔑 **Google Gemini (Free Tier)**

### Setup Instructions
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### Environment Configuration
```bash
# .env file
LLM_PROVIDER=gemini
LLM_MODEL=gemini-pro
GEMINI_API_KEY=your_api_key_here
```

### Available Models
- `gemini-pro` - Text generation
- `gemini-pro-vision` - Image + text processing

### Pros
- ✅ Free tier available
- ✅ High quality responses
- ✅ Good JSON structure adherence
- ✅ Fast response times

### Cons
- ❌ Requires API key
- ❌ Rate limits on free tier
- ❌ Data sent to Google servers

---

## 🤖 **OpenAI GPT (Free Tier: $5/month)**

### Setup Instructions
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add billing information (required even for free tier)

### Environment Configuration
```bash
# .env file
LLM_PROVIDER=openai
LLM_MODEL=gpt-3.5-turbo
OPENAI_API_KEY=your_api_key_here
```

### Available Models
- `gpt-3.5-turbo` - Fast and cost-effective
- `gpt-4` - Highest quality (more expensive)

### Pros
- ✅ Excellent JSON structure adherence
- ✅ Reliable and stable
- ✅ Good documentation

### Cons
- ❌ Requires credit card for free tier
- ❌ Rate limits
- ❌ Data sent to OpenAI servers

---

## 🧠 **Anthropic Claude (Free Tier: $5/month)**

### Setup Instructions
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create a new API key
3. Add billing information

### Environment Configuration
```bash
# .env file
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-haiku-20240307
ANTHROPIC_API_KEY=your_api_key_here
```

### Available Models
- `claude-3-haiku` - Fast and cost-effective
- `claude-3-sonnet` - Higher quality

### Pros
- ✅ Excellent reasoning capabilities
- ✅ Good for complex tasks
- ✅ Strong safety features

### Cons
- ❌ Requires credit card for free tier
- ❌ Rate limits
- ❌ Data sent to Anthropic servers

---

## 🤗 **Hugging Face (Free)**

### Setup Instructions
1. Go to [Hugging Face](https://huggingface.co/settings/tokens)
2. Create a new access token (optional, for higher rate limits)

### Environment Configuration
```bash
# .env file
LLM_PROVIDER=huggingface
LLM_MODEL=microsoft/DialoGPT-medium
HUGGINGFACE_API_KEY=your_token_here  # Optional
```

### Available Models
- `microsoft/DialoGPT-medium` - Conversational
- `gpt2` - Text generation
- `distilbert-base-uncased` - Text classification

### Pros
- ✅ Completely free
- ✅ No credit card required
- ✅ Many model options

### Cons
- ❌ Lower quality than commercial models
- ❌ Limited JSON structure adherence
- ❌ Rate limits on free tier

---

## 🔧 **Configuration Management**

### Switching Between Providers
```python
# In your code
from modules.llm.client import LLMFactory

# Use environment variable or specify directly
llm_client = LLMFactory.create_client("ollama")  # or "gemini", "openai", etc.
```

### Testing Your Setup
```python
# Test script
from modules.llm.client import LLMFactory

def test_llm_setup():
    try:
        llm_client = LLMFactory.create_client()
        response = llm_client.generate("Hello, this is a test.")
        print(f"✅ LLM setup successful: {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ LLM setup failed: {e}")
        return False

if __name__ == "__main__":
    test_llm_setup()
```

### Environment File Template
```bash
# .env
# Database
DATABASE_URL=postgresql://user:pass@localhost/bevscan

# LLM Configuration
LLM_PROVIDER=ollama
LLM_MODEL=llama3.1:8b

# API Keys (only for cloud providers)
GEMINI_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
HUGGINGFACE_API_KEY=

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434

# Other settings...
JWT_SECRET=your-secret-key
UPLOAD_DIR=./uploads
```

---

## 🚀 **Quick Start Recommendations**

### For Development/Testing
1. **Start with Ollama** - No setup complexity, completely free
2. **Use `llama3.1:8b` model** - Good balance of quality and speed

### For Production
1. **Use Gemini** - Free tier, high quality, good JSON adherence
2. **Fallback to Ollama** - For cost control and privacy

### For Maximum Quality
1. **Use GPT-4** - Best JSON structure adherence
2. **Use Claude-3-Sonnet** - Best reasoning capabilities

---

## 🛠️ **Troubleshooting**

### Ollama Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama service
sudo systemctl restart ollama

# Check available models
ollama list
```

### API Key Issues
```bash
# Test API key (replace with your provider)
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.openai.com/v1/models
```

### Model Download Issues
```bash
# For Ollama, check disk space
df -h

# For cloud providers, check network
ping api.openai.com
```

---

## 📊 **Cost Comparison**

| Provider | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| Ollama | ✅ Unlimited | N/A | Development, Privacy |
| Gemini | ✅ Free | Pay-per-use | Production, Quality |
| OpenAI | $5/month | Pay-per-use | Maximum Quality |
| Anthropic | $5/month | Pay-per-use | Complex Reasoning |
| Hugging Face | ✅ Free | Pay-per-use | Experimentation | 