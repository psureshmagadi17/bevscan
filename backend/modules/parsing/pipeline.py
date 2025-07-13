"""
Main parsing pipeline for invoice processing
Orchestrates OCR → Text Preprocessing → LLM Extraction → Validation
"""

import json
import structlog
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime

from modules.ocr.engine import OCREngine
from modules.llm.client import LLMFactory
from modules.parsing.validators.price_validator import PriceValidator
from modules.parsing.validators.duplicate_validator import DuplicateValidator
from app.config import settings

logger = structlog.get_logger()

class InvoiceParsingPipeline:
    """Main invoice parsing pipeline"""
    
    def __init__(self, llm_provider: str = None, llm_model: str = None):
        self.ocr_engine = OCREngine()
        
        # Use provided LLM provider/model or fall back to settings
        if llm_provider:
            self.llm_client = LLMFactory.create_client(llm_provider, llm_model)
        else:
            self.llm_client = LLMFactory.create_client(settings.LLM_PROVIDER, settings.LLM_MODEL)
            
        self.price_validator = PriceValidator()
        self.duplicate_validator = DuplicateValidator()
        
    async def parse_invoice(self, file_path: str) -> Dict[str, Any]:
        """
        Parse invoice from file path
        Returns: Parsed invoice data with confidence scores
        """
        print("🚀 [DEBUG] Starting invoice parsing for:", file_path)
        logger.info(f"Starting invoice parsing for {file_path}")
        
        try:
            # Step 1: OCR Processing
            print("🔍 [DEBUG] Starting OCR extraction...")
            ocr_result = await self._extract_text(file_path)
            print("🔍 [DEBUG] OCR result:", ocr_result)
            if not ocr_result['success']:
                print("❌ [DEBUG] OCR failed:", ocr_result.get('error'))
                return {
                    'success': False,
                    'error': 'OCR extraction failed',
                    'details': ocr_result.get('error')
                }
            
            raw_text = ocr_result['text']
            ocr_confidence = ocr_result['confidence']
            print("🔍 [DEBUG] OCR extracted text:\n", raw_text[:1000])
            
            # Step 2: Text Preprocessing
            processed_text = self._preprocess_text(raw_text)
            
            # Step 3: LLM Extraction
            print("🤖 [DEBUG] LLM prompt/input:\n", processed_text[:1000])
            llm_result = await self._extract_structured_data(processed_text)
            if not llm_result['success']:
                return {
                    'success': False,
                    'error': 'LLM extraction failed',
                    'details': llm_result.get('error')
                }
            
            parsed_data = llm_result['data']
            llm_confidence = llm_result['confidence']
            
            # Convert data types (strings to numbers)
            parsed_data = self._convert_data_types(parsed_data)
            
            # Step 4: Data Validation
            validation_result = await self._validate_data(parsed_data)
            
            # Step 5: Calculate overall confidence
            overall_confidence = (ocr_confidence + llm_confidence) / 2
            
            # Step 6: Prepare final result
            result = {
                'success': True,
                'raw_text': raw_text,
                'parsed_data': parsed_data,
                'confidence_score': overall_confidence,
                'ocr_confidence': ocr_confidence,
                'llm_confidence': llm_confidence,
                'validation_alerts': validation_result['alerts'],
                'processing_time': datetime.utcnow().isoformat()
            }
            
            logger.info(f"Invoice parsing completed successfully", 
                       confidence=overall_confidence,
                       vendor=parsed_data.get('vendor_name'))
            
            return result
            
        except Exception as e:
            logger.error(f"Invoice parsing failed: {e}", exc_info=True)
            return {
                'success': False,
                'error': 'Pipeline processing failed',
                'details': str(e)
            }
    
    async def _extract_text(self, file_path: str) -> Dict[str, Any]:
        """Extract text from invoice using OCR"""
        try:
            result = await self.ocr_engine.extract_text(file_path)
            return result
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess OCR text for better LLM extraction"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove common OCR artifacts
        text = text.replace('|', 'I')  # Common OCR mistake
        text = text.replace('0', 'O')  # Context-dependent
        
        # Add structure hints
        text = f"INVOICE TEXT:\n{text}\n\nPlease extract structured data from this invoice."
        
        return text
    
    async def _extract_structured_data(self, text: str) -> Dict[str, Any]:
        """Extract structured data using LLM"""
        try:
            # Define the expected JSON schema
            schema = {
                "vendor_name": "string",
                "invoice_number": "string", 
                "invoice_date": "YYYY-MM-DD",
                "due_date": "YYYY-MM-DD or null",
                "items": [
                    {
                        "description": "string",
                        "quantity": "number (not string)",
                        "unit_price": "number (not string)",
                        "total": "number (not string)"
                    }
                ],
                "subtotal": "number (not string)",
                "tax": "number (not string)",
                "total": "number (not string)"
            }
            
            # Create optimized prompt
            prompt = f"""Extract invoice data as JSON:

{text}

Return ONLY valid JSON matching this schema (no other text):
{json.dumps(schema, indent=2)}"""
            
            # Use LLM to extract structured data
            response = self.llm_client.generate_structured(prompt, schema)
            print("🤖 [DEBUG] LLM output:\n", response)
            
            # Validate the response structure
            if self._validate_parsed_data(response):
                return {
                    'success': True,
                    'data': response,
                    'confidence': 0.9  # High confidence for structured extraction
                }
            else:
                return {
                    'success': False,
                    'error': 'Invalid data structure returned by LLM'
                }
                
        except Exception as e:
            logger.error(f"LLM extraction failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _validate_parsed_data(self, data: Dict[str, Any]) -> bool:
        """Validate the structure of parsed data"""
        required_fields = ['vendor_name', 'invoice_number', 'invoice_date', 'total']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return False
        
        # Validate items structure
        if 'items' in data and isinstance(data['items'], list):
            for item in data['items']:
                if not isinstance(item, dict):
                    return False
                if 'description' not in item or 'total' not in item:
                    return False
        
        return True
    
    def _convert_data_types(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert string values to appropriate data types"""
        try:
            # Convert numeric fields
            if 'total' in data and data['total']:
                data['total'] = float(str(data['total']).replace('$', '').replace(',', ''))
            if 'subtotal' in data and data['subtotal']:
                data['subtotal'] = float(str(data['subtotal']).replace('$', '').replace(',', ''))
            if 'tax' in data and data['tax']:
                data['tax'] = float(str(data['tax']).replace('$', '').replace(',', ''))
            
            # Convert item fields
            if 'items' in data and isinstance(data['items'], list):
                for item in data['items']:
                    if 'quantity' in item and item['quantity']:
                        # Handle non-numeric quantities like "I" (OCR artifact)
                        try:
                            item['quantity'] = float(item['quantity'])
                        except (ValueError, TypeError):
                            item['quantity'] = 1.0  # Default to 1 if can't parse
                    
                    if 'unit_price' in item and item['unit_price']:
                        item['unit_price'] = float(str(item['unit_price']).replace('$', '').replace(',', ''))
                    
                    if 'total' in item and item['total']:
                        item['total'] = float(str(item['total']).replace('$', '').replace(',', ''))
            
            return data
        except Exception as e:
            logger.error(f"Data type conversion failed: {e}")
            return data  # Return original data if conversion fails
    
    async def _validate_data(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate extracted data and generate alerts"""
        alerts = []
        
        try:
            # Price validation
            price_alerts = await self.price_validator.validate(parsed_data)
            alerts.extend(price_alerts)
            
            # Duplicate validation
            duplicate_alerts = await self.duplicate_validator.validate(parsed_data)
            alerts.extend(duplicate_alerts)
            
        except Exception as e:
            logger.error(f"Data validation failed: {e}")
            alerts.append({
                'type': 'validation_error',
                'message': f'Validation process failed: {str(e)}',
                'severity': 'high'
            })
        
        return {'alerts': alerts}
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return {
            'ocr_engine': self.ocr_engine.get_stats(),
            'llm_provider': self.llm_client.__class__.__name__,
            'validators': [
                'price_validator',
                'duplicate_validator'
            ]
        } 