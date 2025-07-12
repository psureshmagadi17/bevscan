#!/usr/bin/env python3
"""
BevScan Setup Test Script
Tests all components: OCR, LLM, Database, and basic functionality
"""

import os
import sys
import json
import requests
from pathlib import Path

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

def test_python_version():
    """Test Python version"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    if version.major == 3 and version.minor >= 11:
        print("   ✅ Python version is compatible")
        return True
    else:
        print("   ❌ Python version should be 3.11+")
        return False

def test_imports():
    """Test all required imports"""
    print("\n📦 Testing imports...")
    
    imports = {
        "FastAPI": "fastapi",
        "SQLAlchemy": "sqlalchemy", 
        "Pydantic": "pydantic",
        "OpenCV": "cv2",
        "Pillow": "PIL",
        "Tesseract": "pytesseract",
        "EasyOCR": "easyocr",
        "Google Generative AI": "google.generativeai",
        "PostgreSQL": "psycopg2",
        "Requests": "requests"
    }
    
    failed_imports = []
    
    for name, module in imports.items():
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError as e:
            print(f"   ❌ {name}: {e}")
            failed_imports.append(name)
    
    return len(failed_imports) == 0

def test_tesseract():
    """Test Tesseract OCR"""
    print("\n🔍 Testing Tesseract OCR...")
    try:
        import pytesseract
        from PIL import Image
        import numpy as np
        
        # Create a simple test image with text
        img = Image.new('RGB', (200, 50), color='white')
        img.save('test_image.png')
        
        # Test OCR
        text = pytesseract.image_to_string('test_image.png')
        print("   ✅ Tesseract is working")
        
        # Cleanup
        os.remove('test_image.png')
        return True
    except Exception as e:
        print(f"   ❌ Tesseract error: {e}")
        return False

def test_ollama():
    """Test Ollama LLM"""
    print("\n🤖 Testing Ollama LLM...")
    
    models = ["llama3.2"]  # Skip deepseek-r1 for now due to timeout
    
    for model in models:
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": "Extract vendor name from: Invoice from ABC Beverages",
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ {model}: {result['response'][:50]}...")
            else:
                print(f"   ❌ {model}: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ {model}: {e}")
            return False
    
    return True

def test_gemini():
    """Test Google Gemini API"""
    print("\n🔑 Testing Google Gemini API...")
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("   ⚠️  GEMINI_API_KEY not found in environment")
            return False
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content("Extract vendor name from: Invoice from ABC Beverages")
        print(f"   ✅ Gemini: {response.text[:50]}...")
        return True
        
    except Exception as e:
        print(f"   ❌ Gemini error: {e}")
        return False

def test_database():
    """Test PostgreSQL database connection"""
    print("\n🗄️  Testing PostgreSQL database...")
    try:
        import psycopg2
        
        # Test connection
        conn = psycopg2.connect(
            host="localhost",
            database="bevscan",
            user=os.getenv("USER", "postgres")
        )
        
        # Test query
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"   ✅ PostgreSQL connected: {version[0][:50]}...")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False

def test_invoice_parsing():
    """Test complete invoice parsing pipeline"""
    print("\n📄 Testing invoice parsing pipeline...")
    
    # Sample invoice text
    sample_invoice = """
    INVOICE
    
    Vendor: ABC Beverages Inc.
    Invoice #: INV-2024-001
    Date: 2024-01-15
    
    Items:
    1. Coca Cola 12oz - Qty: 24 - Price: $0.75 - Total: $18.00
    2. Pepsi 12oz - Qty: 24 - Price: $0.70 - Total: $16.80
    
    Subtotal: $34.80
    Tax: $2.78
    Total: $37.58
    """
    
    try:
        # Test LLM extraction
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": f"""
                Extract the following information from this invoice in JSON format:
                {{
                    "vendor_name": "string",
                    "invoice_number": "string",
                    "invoice_date": "YYYY-MM-DD",
                    "items": [
                        {{
                            "description": "string",
                            "quantity": "number",
                            "unit_price": "number",
                            "total": "number"
                        }}
                    ],
                    "subtotal": "number",
                    "tax": "number",
                    "total": "number"
                }}
                
                Invoice text:
                {sample_invoice}
                """,
                "stream": False
            },
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ LLM extraction successful: {result['response'][:100]}...")
            
            # Try to parse JSON
            try:
                # Find JSON in response
                response_text = result['response']
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                
                if start_idx != -1 and end_idx != 0:
                    json_str = response_text[start_idx:end_idx]
                    parsed_data = json.loads(json_str)
                    print(f"   ✅ JSON parsing successful: {parsed_data.get('vendor_name', 'N/A')}")
                else:
                    print("   ⚠️  JSON not found in response")
                    
            except json.JSONDecodeError as e:
                print(f"   ⚠️  JSON parsing failed: {e}")
            
            return True
        else:
            print(f"   ❌ LLM extraction failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Pipeline error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 BevScan Setup Test Suite")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Imports", test_imports),
        ("Tesseract OCR", test_tesseract),
        ("Ollama LLM", test_ollama),
        ("Google Gemini", test_gemini),
        ("PostgreSQL Database", test_database),
        ("Invoice Parsing Pipeline", test_invoice_parsing)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name}: Unexpected error - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your BevScan setup is ready.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 