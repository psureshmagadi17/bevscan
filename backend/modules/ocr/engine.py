"""
OCR Engine for text extraction from invoice images and PDFs
Supports multiple OCR backends with fallback mechanisms
"""

import os
import structlog
from typing import Dict, Any, Optional
from pathlib import Path
import asyncio

from .tesseract_engine import TesseractEngine
from .easyocr_engine import EasyOCREngine
from .preprocessing import ImagePreprocessor

logger = structlog.get_logger()

class OCREngine:
    """Main OCR engine with multiple backend support"""
    
    def __init__(self, primary_engine: str = "tesseract"):
        self.primary_engine = primary_engine
        self.preprocessor = ImagePreprocessor()
        
        # Initialize OCR engines
        self.tesseract = TesseractEngine()
        self.easyocr = EasyOCREngine()
        
        # Statistics
        self.stats = {
            'total_processed': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'average_confidence': 0.0
        }
    
    async def extract_text(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text from file (image or PDF)
        Returns: Dict with text, confidence, and metadata
        """
        logger.info(f"Starting OCR extraction for {file_path}")
        
        try:
            # Validate file
            if not self._validate_file(file_path):
                return {
                    'success': False,
                    'error': 'Invalid file format or file not found'
                }
            
            # Preprocess image
            processed_path = await self._preprocess_image(file_path)
            
            # Try primary OCR engine
            result = await self._extract_with_engine(processed_path, self.primary_engine)
            
            # If primary fails, try fallback
            if not result['success'] and self.primary_engine != "easyocr":
                logger.info("Primary OCR failed, trying EasyOCR fallback")
                result = await self._extract_with_engine(processed_path, "easyocr")
            
            # Update statistics
            self._update_stats(result)
            
            # Cleanup processed file if it's different from original
            if processed_path != file_path and os.path.exists(processed_path):
                os.remove(processed_path)
            
            return result
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }
    
    def _validate_file(self, file_path: str) -> bool:
        """Validate file exists and is supported format"""
        if not os.path.exists(file_path):
            return False
        
        # Check file extension
        supported_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp']
        file_ext = Path(file_path).suffix.lower()
        
        return file_ext in supported_extensions
    
    async def _preprocess_image(self, file_path: str) -> str:
        """Preprocess image for better OCR results"""
        try:
            # For now, return original path
            # TODO: Implement image preprocessing (denoising, deskewing, etc.)
            return file_path
        except Exception as e:
            logger.warning(f"Image preprocessing failed: {e}")
            return file_path
    
    async def _extract_with_engine(self, file_path: str, engine_name: str) -> Dict[str, Any]:
        """Extract text using specific OCR engine"""
        try:
            if engine_name == "tesseract":
                return await self.tesseract.extract_text(file_path)
            elif engine_name == "easyocr":
                return await self.easyocr.extract_text(file_path)
            else:
                return {
                    'success': False,
                    'error': f'Unknown OCR engine: {engine_name}'
                }
        except Exception as e:
            logger.error(f"OCR engine {engine_name} failed: {e}")
            return {
                'success': False,
                'error': f'{engine_name} extraction failed: {str(e)}'
            }
    
    def _update_stats(self, result: Dict[str, Any]):
        """Update OCR statistics"""
        self.stats['total_processed'] += 1
        
        if result['success']:
            self.stats['successful_extractions'] += 1
            confidence = result.get('confidence', 0.0)
            
            # Update average confidence
            current_avg = self.stats['average_confidence']
            total_successful = self.stats['successful_extractions']
            self.stats['average_confidence'] = (
                (current_avg * (total_successful - 1) + confidence) / total_successful
            )
        else:
            self.stats['failed_extractions'] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get OCR engine statistics"""
        return {
            'primary_engine': self.primary_engine,
            'total_processed': self.stats['total_processed'],
            'successful_extractions': self.stats['successful_extractions'],
            'failed_extractions': self.stats['failed_extractions'],
            'success_rate': (
                self.stats['successful_extractions'] / max(self.stats['total_processed'], 1)
            ),
            'average_confidence': self.stats['average_confidence']
        }
    
    def get_supported_formats(self) -> list:
        """Get list of supported file formats"""
        return ['.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp']
    
    def get_available_engines(self) -> list:
        """Get list of available OCR engines"""
        engines = []
        
        if self.tesseract.is_available():
            engines.append('tesseract')
        
        if self.easyocr.is_available():
            engines.append('easyocr')
        
        return engines 