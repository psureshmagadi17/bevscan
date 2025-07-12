#!/usr/bin/env python3
"""
Test script for core BevScan modules
"""

import asyncio
import sys
from pathlib import Path

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

async def test_core_modules():
    """Test core modules functionality"""
    print("🧪 Testing Core Modules")
    print("=" * 50)
    
    try:
        # Test imports
        print("📦 Testing imports...")
        
        from modules.parsing.pipeline import InvoiceParsingPipeline
        from modules.ocr.engine import OCREngine
        from modules.llm.client import LLMFactory
        from app.core.models.invoice import Invoice, Vendor, InvoiceItem, Alert
        from app.core.schemas.invoice import InvoiceCreate, VendorCreate
        
        print("   ✅ All core modules imported successfully")
        
        # Test OCR engine
        print("\n🔍 Testing OCR Engine...")
        ocr_engine = OCREngine()
        print(f"   ✅ OCR Engine initialized: {ocr_engine.get_available_engines()}")
        
        # Test LLM client
        print("\n🤖 Testing LLM Client...")
        llm_client = LLMFactory.create_client()
        print(f"   ✅ LLM Client initialized: {llm_client.__class__.__name__}")
        
        # Test parsing pipeline
        print("\n📄 Testing Parsing Pipeline...")
        pipeline = InvoiceParsingPipeline()
        print(f"   ✅ Parsing Pipeline initialized")
        
        # Test database models
        print("\n🗄️  Testing Database Models...")
        vendor = Vendor(name="Test Vendor", email="test@example.com")
        invoice = Invoice(
            vendor_id=1,
            invoice_number="TEST-001",
            invoice_date="2024-01-15",
            total=100.00
        )
        print(f"   ✅ Database models created: {vendor.name}, {invoice.invoice_number}")
        
        # Test Pydantic schemas
        print("\n📋 Testing Pydantic Schemas...")
        vendor_schema = VendorCreate(name="Test Vendor", email="test@example.com")
        invoice_schema = InvoiceCreate(
            vendor_id=1,
            invoice_number="TEST-001",
            invoice_date="2024-01-15",
            total=100.00
        )
        print(f"   ✅ Pydantic schemas created: {vendor_schema.name}, {invoice_schema.invoice_number}")
        
        print("\n🎉 All core modules are working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Core modules test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_simple_parsing():
    """Test simple parsing with sample text"""
    print("\n🧪 Testing Simple Parsing")
    print("=" * 50)
    
    try:
        from modules.llm.client import LLMFactory
        
        # Create LLM client (force Gemini)
        llm_client = LLMFactory.create_client("gemini")
        
        # Sample invoice text
        sample_text = """
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
        
        # Test LLM extraction
        schema = {
            "vendor_name": "string",
            "invoice_number": "string",
            "invoice_date": "YYYY-MM-DD",
            "items": [
                {
                    "description": "string",
                    "quantity": "number",
                    "unit_price": "number",
                    "total": "number"
                }
            ],
            "subtotal": "number",
            "tax": "number",
            "total": "number"
        }
        
        prompt = f"""
        Extract the following information from this invoice text in valid JSON format:
        
        {schema}
        
        Invoice text:
        {sample_text}
        
        Important: Respond only with valid JSON. Do not include any explanations or additional text.
        """
        
        print("📝 Testing LLM extraction...")
        response = llm_client.generate_structured(prompt, schema)
        
        print(f"   ✅ LLM extraction successful")
        print(f"   📊 Vendor: {response.get('vendor_name', 'N/A')}")
        print(f"   📊 Invoice: {response.get('invoice_number', 'N/A')}")
        print(f"   📊 Total: ${response.get('total', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Simple parsing test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("🚀 BevScan Core Modules Test Suite")
    print("=" * 60)
    
    # Test core modules
    core_success = await test_core_modules()
    
    # Test simple parsing
    parsing_success = await test_simple_parsing()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    print(f"{'✅ PASS' if core_success else '❌ FAIL'} Core Modules")
    print(f"{'✅ PASS' if parsing_success else '❌ FAIL'} Simple Parsing")
    
    total_tests = 2
    passed_tests = sum([core_success, parsing_success])
    
    print(f"\n🎯 Overall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Core modules are ready for development.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 