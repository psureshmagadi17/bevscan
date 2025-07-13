#!/usr/bin/env python3
"""
Direct test of the parsing pipeline
"""

import asyncio
import os
from pathlib import Path
from modules.parsing.pipeline import InvoiceParsingPipeline

async def test_pipeline():
    """Test the pipeline directly"""
    print("🚀 Testing Pipeline Directly")
    print("=" * 50)
    
    # Get the sample invoice path
    file_path = Path(__file__).parent / "uploads" / "sample_beverage_invoice.pdf"
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return
    
    print(f"📄 Testing with file: {file_path}")
    
    try:
        # Create pipeline
        pipeline = InvoiceParsingPipeline()
        
        # Parse the invoice
        print("🔍 Starting pipeline...")
        result = await pipeline.parse_invoice(str(file_path))
        
        print("📊 Pipeline Result:")
        print(f"   Success: {result.get('success')}")
        print(f"   Error: {result.get('error')}")
        print(f"   Raw Text Length: {len(result.get('raw_text', ''))}")
        print(f"   Parsed Data: {result.get('parsed_data')}")
        print(f"   Confidence: {result.get('confidence_score')}")
        
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_pipeline()) 