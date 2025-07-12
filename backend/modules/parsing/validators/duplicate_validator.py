"""
Duplicate validation module
Checks for duplicate invoice numbers and similar invoices
"""

import structlog
from typing import Dict, Any, List
from datetime import datetime

logger = structlog.get_logger()

class DuplicateValidator:
    """Validates invoices for duplicates"""
    
    def __init__(self):
        self.processed_invoices = set()  # In-memory cache, should be replaced with DB
    
    async def validate(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validate for duplicate invoices
        Returns: List of alerts for duplicates
        """
        alerts = []
        
        try:
            invoice_number = parsed_data.get('invoice_number')
            vendor_name = parsed_data.get('vendor_name', 'Unknown')
            invoice_date = parsed_data.get('invoice_date')
            total = parsed_data.get('total')
            
            if not invoice_number:
                alerts.append({
                    'type': 'missing_invoice_number',
                    'message': 'Invoice number is missing',
                    'severity': 'high'
                })
                return alerts
            
            # Check for exact duplicate invoice number
            if await self._is_duplicate_invoice_number(invoice_number, vendor_name):
                alerts.append({
                    'type': 'duplicate_invoice_number',
                    'message': f'Duplicate invoice number detected: {invoice_number}',
                    'severity': 'high',
                    'details': {
                        'invoice_number': invoice_number,
                        'vendor': vendor_name
                    }
                })
            
            # Check for similar invoices (same vendor, date, and total)
            similar_invoices = await self._find_similar_invoices(vendor_name, invoice_date, total)
            if similar_invoices:
                alerts.append({
                    'type': 'similar_invoice',
                    'message': f'Similar invoice found for {vendor_name} on {invoice_date}',
                    'severity': 'medium',
                    'details': {
                        'vendor': vendor_name,
                        'date': invoice_date,
                        'total': total,
                        'similar_count': len(similar_invoices)
                    }
                })
            
            # Add to processed invoices
            self._add_processed_invoice(invoice_number, vendor_name, invoice_date, total)
            
            logger.info(f"Duplicate validation completed for {vendor_name}", 
                       alerts_count=len(alerts))
            
            return alerts
            
        except Exception as e:
            logger.error(f"Duplicate validation failed: {e}")
            return [{
                'type': 'duplicate_validation_error',
                'message': f'Duplicate validation process failed: {str(e)}',
                'severity': 'high'
            }]
    
    async def _is_duplicate_invoice_number(self, invoice_number: str, vendor_name: str) -> bool:
        """
        Check if invoice number already exists for this vendor
        TODO: Replace with actual database query
        """
        # This is a placeholder - should query the database
        # For now, check in-memory cache
        key = f"{vendor_name}:{invoice_number}"
        return key in self.processed_invoices
    
    async def _find_similar_invoices(self, vendor_name: str, invoice_date: str, total: float) -> List[Dict[str, Any]]:
        """
        Find similar invoices (same vendor, date, and similar total)
        TODO: Replace with actual database query
        """
        # This is a placeholder - should query the database
        # For now, return empty list
        return []
    
    def _add_processed_invoice(self, invoice_number: str, vendor_name: str, 
                             invoice_date: str, total: float):
        """Add invoice to processed set (for testing purposes)"""
        key = f"{vendor_name}:{invoice_number}"
        self.processed_invoices.add(key)
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Get validation statistics"""
        return {
            'processed_invoices_count': len(self.processed_invoices),
            'validator_type': 'duplicate_validator'
        }
    
    def clear_cache(self):
        """Clear the processed invoices cache (for testing)"""
        self.processed_invoices.clear() 