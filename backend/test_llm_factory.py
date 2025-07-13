#!/usr/bin/env python3
"""
Test LLM factory to see which provider is being selected
"""

import os
from modules.llm.client import LLMFactory

def test_llm_factory():
    """Test the LLM factory"""
    print("🔍 Testing LLM Factory")
    print("=" * 30)
    
    print(f"LLM_PROVIDER env var: {os.getenv('LLM_PROVIDER')}")
    print(f"GEMINI_API_KEY env var: {'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET'}")
    
    try:
        # Create client
        client = LLMFactory.create_client()
        print(f"✅ Created client: {type(client).__name__}")
        
        # Test a simple generation
        print("🧪 Testing simple generation...")
        response = client.generate("Hello, how are you?")
        print(f"✅ Response: {response[:100]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_llm_factory() 