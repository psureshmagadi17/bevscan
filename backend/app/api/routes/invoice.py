from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.models.invoice import Invoice, Vendor, InvoiceItem, Alert
from app.core.schemas.invoice import InvoiceResponse
from app.config import settings
from modules.parsing.pipeline import InvoiceParsingPipeline
import os
from pathlib import Path
import shutil
from typing import List
import structlog
from datetime import datetime

logger = structlog.get_logger()
router = APIRouter(prefix="/invoices", tags=["invoices"])

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload", status_code=status.HTTP_201_CREATED)
def upload_invoice(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload an invoice file (PDF/image) and create a DB record."""
    # Save file to uploads directory
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    save_path = UPLOAD_DIR / file.filename
    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Create placeholder DB record (expand as needed)
    invoice = Invoice(
        vendor_id=1,  # TODO: Replace with actual vendor logic
        invoice_number=file.filename,
        invoice_date=datetime.now().date(),  # Use current date as placeholder
        total=None,
        raw_text=None,
        parsed_data=None,
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return {"message": "File uploaded successfully", "invoice_id": invoice.id}

@router.post("/{invoice_id}/parse", status_code=status.HTTP_200_OK)
async def parse_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """Parse an uploaded invoice using OCR and LLM."""
    # Get invoice from database
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found.")
    
    # Find the uploaded file
    file_path = UPLOAD_DIR / invoice.invoice_number
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Invoice file not found.")
    
    try:
        # Initialize parsing pipeline
        pipeline = InvoiceParsingPipeline()
        
        # Parse the invoice
        result = await pipeline.parse_invoice(str(file_path))
        
        # Update invoice with parsed data
        invoice.raw_text = result.get("raw_text")
        invoice.parsed_data = result.get("parsed_data")
        invoice.confidence_score = result.get("confidence_score", 0.0)
        invoice.status = "parsed"
        
        # Update basic fields if available
        if result.get("parsed_data"):
            parsed = result["parsed_data"]
            invoice.invoice_date = parsed.get("invoice_date")
            invoice.total = parsed.get("total")
            invoice.subtotal = parsed.get("subtotal")
            invoice.tax = parsed.get("tax")
        
        db.commit()
        db.refresh(invoice)
        
        return {"message": "Invoice parsed successfully", "invoice_id": invoice_id}
        
    except Exception as e:
        logger.error(f"Error parsing invoice {invoice_id}: {e}")
        raise HTTPException(status_code=500, detail="Error parsing invoice.")

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """Get parsed invoice details."""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found.")
    
    return invoice

@router.get("/", response_model=List[InvoiceResponse])
def list_invoices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all invoices with pagination."""
    invoices = db.query(Invoice).offset(skip).limit(limit).all()
    return invoices 