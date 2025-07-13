#!/usr/bin/env python3
"""
End-to-end test for BevScan pipeline
"""

import requests
import json
import time
import os
from pathlib import Path

# API base URL
API_BASE = "http://localhost:8000"

def test_health():
    """Test API health"""
    print("🏥 Testing API health...")
    response = requests.get(f"{API_BASE}/health")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ API healthy: {data}")
        return True
    else:
        print(f"   ❌ API health check failed: {response.status_code}")
        return False

def test_upload_invoice():
    """Test invoice upload"""
    print("\n📤 Testing invoice upload...")
    
    # Path to sample invoice
    invoice_path = os.path.join(os.path.dirname(__file__), "uploads/sample_beverage_invoice.pdf")
    
    if not os.path.exists(invoice_path):
        print(f"   ❌ Sample invoice not found: {invoice_path}")
        return None
    
    # Upload file
    with open(invoice_path, 'rb') as f:
        files = {'file': ('sample_beverage_invoice.pdf', f, 'application/pdf')}
        response = requests.post(f"{API_BASE}/invoices/upload", files=files)
    
    if response.status_code == 201:
        data = response.json()
        invoice_id = data['invoice_id']
        print(f"   ✅ Invoice uploaded successfully: ID {invoice_id}")
        return invoice_id
    else:
        print(f"   ❌ Upload failed: {response.status_code} - {response.text}")
        return None

def test_parse_invoice(invoice_id):
    """Test invoice parsing"""
    print(f"\n🔍 Testing invoice parsing for ID {invoice_id}...")
    
    response = requests.post(f"{API_BASE}/invoices/{invoice_id}/parse")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Invoice parsed successfully: {data}")
        return True
    else:
        print(f"   ❌ Parsing failed: {response.status_code} - {response.text}")
        return False

def test_get_invoice(invoice_id):
    """Test getting parsed invoice"""
    print(f"\n📋 Testing invoice retrieval for ID {invoice_id}...")
    
    response = requests.get(f"{API_BASE}/invoices/{invoice_id}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Invoice retrieved successfully")
        print(f"   📄 Invoice Number: {data.get('invoice_number', 'N/A')}")
        print(f"   📅 Status: {data.get('status', 'N/A')}")
        print(f"   💰 Total: {data.get('total', 'N/A')}")
        print(f"   🎯 Confidence: {data.get('confidence_score', 'N/A')}")
        
        if data.get('parsed_data'):
            print(f"   📊 Parsed data available: {len(str(data['parsed_data']))} characters")
        
        return data
    else:
        print(f"   ❌ Retrieval failed: {response.status_code} - {response.text}")
        return None

def test_list_invoices():
    """Test listing invoices"""
    print("\n📋 Testing invoice list...")
    
    response = requests.get(f"{API_BASE}/invoices/")
    
    if response.status_code == 200:
        invoices = response.json()
        print(f"   ✅ Found {len(invoices)} invoices")
        for invoice in invoices:
            print(f"      - ID {invoice['id']}: {invoice['invoice_number']} ({invoice['status']})")
        return invoices
    else:
        print(f"   ❌ List failed: {response.status_code} - {response.text}")
        return []

def main():
    """Run complete end-to-end test"""
    print("🚀 Starting BevScan End-to-End Test")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health():
        print("❌ Health check failed. Make sure the backend is running.")
        return
    
    # Test 2: Upload invoice
    invoice_id = test_upload_invoice()
    if not invoice_id:
        print("❌ Upload failed. Stopping test.")
        return
    
    # Test 3: Parse invoice
    if not test_parse_invoice(invoice_id):
        print("❌ Parsing failed. Stopping test.")
        return
    
    # Wait a moment for processing
    print("\n⏳ Waiting for processing to complete...")
    time.sleep(3)
    
    # Test 4: Get parsed invoice
    invoice_data = test_get_invoice(invoice_id)
    if not invoice_data:
        print("❌ Retrieval failed. Stopping test.")
        return
    
    # Test 5: List all invoices
    test_list_invoices()
    
    print("\n" + "=" * 50)
    print("🎉 End-to-End Test Complete!")
    print(f"📊 Test Results:")
    print(f"   - Invoice ID: {invoice_id}")
    print(f"   - Status: {invoice_data.get('status', 'N/A')}")
    print(f"   - Confidence: {invoice_data.get('confidence_score', 'N/A')}")
    
    if invoice_data.get('parsed_data'):
        print(f"   - Parsed Data: ✅ Available")
    else:
        print(f"   - Parsed Data: ❌ Not available")
    
    print(f"\n🌐 Frontend URL: http://localhost:3000")
    print(f"🔧 Backend API: http://localhost:8000")
    print(f"📚 API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 