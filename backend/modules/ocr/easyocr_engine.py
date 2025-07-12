"""
EasyOCR Engine implementation (placeholder)
"""

import structlog
from typing import Dict, Any

logger = structlog.get_logger()

class EasyOCREngine:
    """EasyOCR engine implementation (placeholder)"""
    
    def __init__(self):
        self.available = False  # Not implemented yet
        logger.warning("EasyOCR engine not implemented yet")
    
    def is_available(self) -> bool:
        """Check if EasyOCR is available"""
        return self.available
    
    async def extract_text(self, file_path: str) -> Dict[str, Any]:
        """Extract text from file using EasyOCR"""
        return {
            'success': False,
            'error': 'EasyOCR not implemented yet'
        } 