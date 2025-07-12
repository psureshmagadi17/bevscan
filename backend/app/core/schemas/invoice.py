from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from decimal import Decimal

# Base schemas
class VendorBase(BaseModel):
    name: str = Field(..., description="Vendor name")
    email: Optional[str] = Field(None, description="Vendor email")
    phone: Optional[str] = Field(None, description="Vendor phone")

class VendorCreate(VendorBase):
    pass

class Vendor(VendorBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class InvoiceItemBase(BaseModel):
    sku: Optional[str] = Field(None, description="Product SKU")
    description: Optional[str] = Field(None, description="Product description")
    quantity: Optional[Decimal] = Field(None, description="Quantity")
    unit_price: Optional[Decimal] = Field(None, description="Unit price")
    total: Optional[Decimal] = Field(None, description="Line total")

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItem(InvoiceItemBase):
    id: int
    invoice_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class InvoiceBase(BaseModel):
    invoice_number: str = Field(..., description="Invoice number")
    invoice_date: date = Field(..., description="Invoice date")
    due_date: Optional[date] = Field(None, description="Due date")
    subtotal: Optional[Decimal] = Field(None, description="Subtotal")
    tax: Optional[Decimal] = Field(None, description="Tax amount")
    total: Optional[Decimal] = Field(None, description="Total amount")

class InvoiceCreate(InvoiceBase):
    vendor_id: int
    raw_text: Optional[str] = Field(None, description="Raw OCR text")
    parsed_data: Optional[Dict[str, Any]] = Field(None, description="Parsed JSON data")
    confidence_score: Optional[Decimal] = Field(None, description="Parsing confidence score")
    items: Optional[List[InvoiceItemCreate]] = Field(None, description="Invoice items")

class Invoice(InvoiceBase):
    id: int
    vendor_id: int
    status: str
    confidence_score: Optional[Decimal]
    raw_text: Optional[str]
    parsed_data: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    
    # Relationships
    vendor: Vendor
    items: List[InvoiceItem] = []
    
    class Config:
        from_attributes = True

class AlertBase(BaseModel):
    alert_type: str = Field(..., description="Type of alert")
    message: str = Field(..., description="Alert message")
    severity: str = Field("medium", description="Alert severity")

class AlertCreate(AlertBase):
    invoice_id: int

class Alert(AlertBase):
    id: int
    invoice_id: int
    status: str
    created_at: datetime
    resolved_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Request/Response schemas
class UploadResponse(BaseModel):
    upload_id: str
    filename: str
    status: str
    message: str

class ParseRequest(BaseModel):
    upload_id: str

class ParseResponse(BaseModel):
    invoice_id: int
    status: str
    confidence_score: Optional[Decimal]
    parsed_data: Optional[Dict[str, Any]]
    alerts: List[Alert] = []

class DashboardSummary(BaseModel):
    total_invoices: int
    total_spend: Decimal
    top_vendors: List[Dict[str, Any]]
    recent_alerts: List[Alert]

class ExportRequest(BaseModel):
    format: str = Field(..., description="Export format (csv/pdf)")
    date_from: Optional[date] = Field(None, description="Start date")
    date_to: Optional[date] = Field(None, description="End date")
    vendor_id: Optional[int] = Field(None, description="Filter by vendor") 

class InvoiceResponse(BaseModel):
    """Invoice response schema for API"""
    id: int
    vendor_id: int
    invoice_number: str
    invoice_date: Optional[date]
    due_date: Optional[date]
    subtotal: Optional[Decimal]
    tax: Optional[Decimal]
    total: Optional[Decimal]
    status: str
    confidence_score: Optional[Decimal]
    raw_text: Optional[str]
    parsed_data: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    
    # Relationships
    vendor: Optional[Vendor] = None
    items: List[InvoiceItem] = []
    alerts: List[Alert] = []
    
    class Config:
        from_attributes = True 

class AlertResponse(BaseModel):
    """Alert response schema for API"""
    id: int
    invoice_id: int
    alert_type: str
    message: str
    severity: str
    status: str
    created_at: datetime
    resolved_at: Optional[datetime]
    
    class Config:
        from_attributes = True 