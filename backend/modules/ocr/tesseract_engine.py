"""
Tesseract OCR Engine implementation
"""

import os
import structlog
from typing import Dict, Any
import asyncio
from pathlib import Path

try:
    import pytesseract
    from PIL import Image
    import pdf2image
except ImportError as e:
    structlog.get_logger().warning(f"Tesseract dependencies not available: {e}")

logger = structlog.get_logger()

class TesseractEngine:
    """Tesseract OCR engine implementation"""
    
    def __init__(self):
        self.available = self._check_availability()
        if self.available:
            logger.info("Tesseract OCR engine initialized")
        else:
            logger.warning("Tesseract OCR engine not available")
    
    def _check_availability(self) -> bool:
        """Check if Tesseract is available"""
        try:
            # Check if tesseract command is available
            import subprocess
            result = subprocess.run(['tesseract', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def is_available(self) -> bool:
        """Check if Tesseract is available"""
        return self.available
    
    async def extract_text(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text from file using Tesseract
        Supports images and PDFs
        """
        print("🔍 [DEBUG] Tesseract: Starting extraction for:", file_path)
        if not self.available:
            print("❌ [DEBUG] Tesseract: Not available")
            return {
                'success': False,
                'error': 'Tesseract not available'
            }
        
        try:
            file_path = Path(file_path)
            
            if file_path.suffix.lower() == '.pdf':
                return await self._extract_from_pdf(file_path)
            else:
                return await self._extract_from_image(file_path)
                
        except Exception as e:
            logger.error(f"Tesseract extraction failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _extract_from_image(self, file_path: Path) -> Dict[str, Any]:
        """Extract text from image file"""
        try:
            # Open image
            image = Image.open(file_path)
            
            # Extract text with confidence
            text = pytesseract.image_to_string(image)
            
            # Get confidence data
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            # Calculate average confidence
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) / 100.0 if confidences else 0.0
            
            return {
                'success': True,
                'text': text.strip(),
                'confidence': avg_confidence,
                'engine': 'tesseract',
                'metadata': {
                    'image_size': image.size,
                    'mode': image.mode,
                    'format': image.format
                }
            }
            
        except Exception as e:
            logger.error(f"Tesseract image extraction failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _extract_from_pdf(self, file_path: Path) -> Dict[str, Any]:
        """Extract text from PDF file"""
        try:
            # Convert PDF to images
            images = pdf2image.convert_from_path(file_path)
            
            if not images:
                return {
                    'success': False,
                    'error': 'No pages found in PDF'
                }
            
            # Extract text from all pages
            all_text = []
            total_confidence = 0.0
            page_count = 0
            
            for i, image in enumerate(images):
                # Extract text from page
                text = pytesseract.image_to_string(image)
                all_text.append(f"--- Page {i+1} ---\n{text}")
                
                # Get confidence for this page
                data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
                confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
                
                if confidences:
                    page_confidence = sum(confidences) / len(confidences) / 100.0
                    total_confidence += page_confidence
                    page_count += 1
            
            # Calculate average confidence across all pages
            avg_confidence = total_confidence / page_count if page_count > 0 else 0.0
            
            return {
                'success': True,
                'text': '\n\n'.join(all_text).strip(),
                'confidence': avg_confidence,
                'engine': 'tesseract',
                'metadata': {
                    'pages': len(images),
                    'file_size': file_path.stat().st_size
                }
            }
            
        except Exception as e:
            logger.error(f"Tesseract PDF extraction failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_config(self) -> Dict[str, Any]:
        """Get Tesseract configuration"""
        try:
            # Get Tesseract version
            import subprocess
            result = subprocess.run(['tesseract', '--version'], 
                                  capture_output=True, text=True)
            version = result.stdout.split('\n')[0] if result.stdout else 'Unknown'
            
            return {
                'engine': 'tesseract',
                'version': version,
                'available': self.available,
                'supported_languages': self._get_supported_languages()
            }
        except Exception as e:
            logger.error(f"Error getting Tesseract config: {e}")
            return {
                'engine': 'tesseract',
                'available': self.available,
                'error': str(e)
            }
    
    def _get_supported_languages(self) -> list:
        """Get list of supported languages"""
        try:
            import subprocess
            result = subprocess.run(['tesseract', '--list-langs'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                return [lang.strip() for lang in lines if lang.strip()]
            else:
                return ['eng']  # Default to English
        except Exception:
            return ['eng']  # Default to English 