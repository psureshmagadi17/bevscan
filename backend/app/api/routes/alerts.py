from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.models.invoice import Alert, Invoice
from app.core.schemas.invoice import AlertResponse
from typing import List

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/", response_model=List[AlertResponse])
def list_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all alerts with pagination."""
    alerts = db.query(Alert).offset(skip).limit(limit).all()
    return alerts

@router.get("/invoices/{invoice_id}/alerts", response_model=List[AlertResponse])
def get_invoice_alerts(invoice_id: int, db: Session = Depends(get_db)):
    """Get alerts for a specific invoice."""
    # Check if invoice exists
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found.")
    
    alerts = db.query(Alert).filter(Alert.invoice_id == invoice_id).all()
    return alerts 