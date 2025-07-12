#!/usr/bin/env python3
"""
Setup initial data for BevScan testing
"""

from app.database import SessionLocal
from app.core.models.invoice import Vendor
from datetime import datetime

def setup_initial_data():
    """Create initial data for testing"""
    db = SessionLocal()
    
    try:
        # Check if default vendor exists
        existing_vendor = db.query(Vendor).filter(Vendor.id == 1).first()
        
        if not existing_vendor:
            # Create default vendor
            default_vendor = Vendor(
                id=1,
                name="Beverage Supply Co.",
                email="sales@beveragesupply.com",
                phone="(555) 123-4567"
            )
            db.add(default_vendor)
            db.commit()
            print("✅ Default vendor created")
        else:
            print("✅ Default vendor already exists")
            
    except Exception as e:
        print(f"❌ Error setting up initial data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_initial_data() 