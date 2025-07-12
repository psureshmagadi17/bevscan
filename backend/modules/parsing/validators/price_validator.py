"""
Price validation module
Checks for price discrepancies and unusual pricing patterns
"""

import structlog
from typing import Dict, Any, List
from decimal import Decimal
from datetime import datetime, timedelta

logger = structlog.get_logger()

class PriceValidator:
    """Validates invoice prices against historical data"""
    
    def __init__(self, threshold: float = 0.05):  # 5% threshold
        self.threshold = threshold
        self.price_history = {}  # In-memory cache, should be replaced with DB
    
    async def validate(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validate prices in parsed invoice data
        Returns: List of alerts for price discrepancies
        """
        alerts = []
        
        try:
            vendor_name = parsed_data.get('vendor_name', 'Unknown')
            items = parsed_data.get('items', [])
            
            for item in items:
                item_alerts = await self._validate_item_price(vendor_name, item)
                alerts.extend(item_alerts)
            
            # Validate total amount
            total_alerts = await self._validate_total_amount(parsed_data)
            alerts.extend(total_alerts)
            
            logger.info(f"Price validation completed for {vendor_name}", 
                       alerts_count=len(alerts))
            
            return alerts
            
        except Exception as e:
            logger.error(f"Price validation failed: {e}")
            return [{
                'type': 'price_validation_error',
                'message': f'Price validation process failed: {str(e)}',
                'severity': 'high'
            }]
    
    async def _validate_item_price(self, vendor_name: str, item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Validate individual item price"""
        alerts = []
        
        try:
            description = item.get('description', 'Unknown Item')
            unit_price = item.get('unit_price')
            quantity = item.get('quantity', 1)
            
            if not unit_price:
                return alerts
            
            # Get historical price for this item
            historical_price = await self._get_historical_price(vendor_name, description)
            
            if historical_price:
                price_change = abs(unit_price - historical_price) / historical_price
                
                if price_change > self.threshold:
                    alerts.append({
                        'type': 'price_discrepancy',
                        'message': f'Price change detected for {description}: '
                                 f'${historical_price:.2f} → ${unit_price:.2f} '
                                 f'({price_change:.1%} change)',
                        'severity': 'medium' if price_change < 0.2 else 'high',
                        'details': {
                            'item': description,
                            'old_price': historical_price,
                            'new_price': unit_price,
                            'change_percentage': price_change
                        }
                    })
            
            # Check for unusually high or low prices
            if unit_price > 100:  # Arbitrary threshold
                alerts.append({
                    'type': 'unusual_price',
                    'message': f'Unusually high unit price for {description}: ${unit_price:.2f}',
                    'severity': 'low',
                    'details': {
                        'item': description,
                        'price': unit_price,
                        'threshold': 100
                    }
                })
            
        except Exception as e:
            logger.error(f"Item price validation failed: {e}")
        
        return alerts
    
    async def _validate_total_amount(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Validate total invoice amount"""
        alerts = []
        
        try:
            total = parsed_data.get('total')
            subtotal = parsed_data.get('subtotal', 0)
            tax = parsed_data.get('tax', 0)
            
            if not total:
                return alerts
            
            # Check if total matches subtotal + tax
            calculated_total = subtotal + tax
            if abs(total - calculated_total) > 0.01:  # Allow for rounding differences
                alerts.append({
                    'type': 'total_mismatch',
                    'message': f'Total amount mismatch: calculated ${calculated_total:.2f} vs ${total:.2f}',
                    'severity': 'medium',
                    'details': {
                        'calculated_total': calculated_total,
                        'invoice_total': total,
                        'difference': abs(total - calculated_total)
                    }
                })
            
            # Check for unusually high totals
            if total > 10000:  # Arbitrary threshold
                alerts.append({
                    'type': 'high_total',
                    'message': f'Unusually high invoice total: ${total:.2f}',
                    'severity': 'low',
                    'details': {
                        'total': total,
                        'threshold': 10000
                    }
                })
            
        except Exception as e:
            logger.error(f"Total amount validation failed: {e}")
        
        return alerts
    
    async def _get_historical_price(self, vendor_name: str, item_description: str) -> float:
        """
        Get historical price for an item from the same vendor
        TODO: Replace with actual database query
        """
        # This is a placeholder - should query the database
        # For now, return None to indicate no historical data
        return None
    
    def update_price_history(self, vendor_name: str, item_description: str, price: float):
        """Update price history (for testing purposes)"""
        key = f"{vendor_name}:{item_description}"
        self.price_history[key] = {
            'price': price,
            'timestamp': datetime.utcnow()
        }
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Get validation statistics"""
        return {
            'threshold': self.threshold,
            'price_history_size': len(self.price_history),
            'validator_type': 'price_validator'
        } 