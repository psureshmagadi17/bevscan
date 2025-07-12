# Technical Specification — BevScan MVP (Enhanced)

## Architecture Overview
- **Frontend**: Next.js 14 with React 18 (TypeScript)
- **Backend**: Python 3.11+ with FastAPI
- **Document Processing**: OCR → Preprocessing → LLM Parsing Pipeline (Python)
- **Database**: PostgreSQL 15+ (relational schema for invoices, vendors, SKUs)
- **Deployment**: Vercel (frontend) + Render or Docker-based VPS (backend)
- **AI/ML**: Google Gemini API for structured parsing, Tesseract/EasyOCR for text extraction

---

## MVP File/Component Structure

### Frontend Structure (Next.js + TypeScript)
```
frontend/
├── app/                          # Next.js 14 App Router
│   ├── layout.tsx               # Root layout with providers
│   ├── page.tsx                 # Landing page
│   ├── upload/
│   │   └── page.tsx             # Upload interface
│   ├── dashboard/
│   │   └── page.tsx             # Main dashboard
│   └── api/                     # API routes (if needed)
├── components/
│   ├── ui/                      # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   └── Alert.tsx
│   ├── upload/
│   │   ├── UploadForm.tsx       # Drag & drop interface
│   │   ├── FilePreview.tsx      # Preview uploaded files
│   │   └── UploadProgress.tsx   # Upload status indicator
│   ├── dashboard/
│   │   ├── DashboardHeader.tsx  # Filters and export buttons
│   │   ├── SpendTrends.tsx      # Time-series chart
│   │   ├── VendorSummary.tsx    # Top vendors widget
│   │   ├── ItemSummary.tsx      # Top items widget
│   │   └── AlertPanel.tsx       # Price discrepancy alerts
│   └── common/
│       ├── LoadingSpinner.tsx
│       └── ErrorBoundary.tsx
├── lib/
│   ├── api.ts                   # API client functions
│   ├── utils.ts                 # Utility functions
│   └── types.ts                 # TypeScript interfaces
├── hooks/
│   ├── useUpload.ts             # Upload state management
│   ├── useDashboard.ts          # Dashboard data fetching
│   └── useAlerts.ts             # Alert management
└── styles/
    └── globals.css              # Global styles (Tailwind)
```

### Backend Structure (Python + FastAPI)
```
backend/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Configuration management
│   ├── database.py              # Database connection setup
│   └── dependencies.py          # Dependency injection
├── api/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── upload.py            # File upload endpoints
│   │   ├── parse.py             # Invoice parsing endpoints
│   │   ├── dashboard.py         # Dashboard data endpoints
│   │   ├── alerts.py            # Alert management endpoints
│   │   └── export.py            # Export endpoints
│   └── middleware/
│       ├── __init__.py
│       ├── auth.py              # Authentication middleware
│       └── cors.py              # CORS configuration
├── core/
│   ├── __init__.py
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── invoice.py           # Invoice model
│   │   ├── vendor.py            # Vendor model
│   │   ├── item.py              # Item/SKU model
│   │   └── alert.py             # Alert model
│   ├── schemas/                 # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── invoice.py           # Invoice request/response schemas
│   │   ├── upload.py            # Upload schemas
│   │   └── dashboard.py         # Dashboard schemas
│   └── services/                # Business logic services
│       ├── __init__.py
│       ├── upload_service.py    # File upload handling
│       ├── validation_service.py # Data validation logic
│       └── alert_service.py     # Alert generation
├── modules/                     # Core processing modules
│   ├── __init__.py
│   ├── ocr/                     # OCR Module
│   │   ├── __init__.py
│   │   ├── engine.py            # OCR engine interface
│   │   ├── tesseract_engine.py  # Tesseract implementation
│   │   ├── easyocr_engine.py    # EasyOCR implementation
│   │   └── preprocessing.py     # Image preprocessing utilities
│   ├── llm/                     # LLM Module
│   │   ├── __init__.py
│   │   ├── client.py            # LLM client interface
│   │   ├── gemini_client.py     # Google Gemini implementation
│   │   ├── prompts.py           # Structured prompts
│   │   └── parser.py            # LLM response parsing
│   └── parsing/                 # Parsing Module
│       ├── __init__.py
│       ├── pipeline.py          # Main parsing pipeline
│       ├── extractors/          # Field-specific extractors
│       │   ├── __init__.py
│       │   ├── vendor_extractor.py
│       │   ├── date_extractor.py
│       │   ├── items_extractor.py
│       │   └── totals_extractor.py
│       └── validators/          # Data validation
│           ├── __init__.py
│           ├── price_validator.py
│           └── duplicate_validator.py
├── utils/
│   ├── __init__.py
│   ├── file_utils.py            # File handling utilities
│   ├── image_utils.py           # Image processing utilities
│   └── logger.py                # Logging configuration
└── tests/                       # Test suite
    ├── __init__.py
    ├── test_ocr/
    ├── test_llm/
    ├── test_parsing/
    └── test_api/
```

---

## Core Processing Modules (Detailed)

### 1. OCR Module (`modules/ocr/`)
**Purpose**: Extract raw text from invoice images/PDFs

**Key Components**:
- `engine.py`: Abstract OCR engine interface
- `tesseract_engine.py`: Tesseract OCR implementation
- `easyocr_engine.py`: EasyOCR implementation (backup)
- `preprocessing.py`: Image enhancement utilities

**Features**:
- Image preprocessing (denoising, deskewing, contrast enhancement)
- Multi-language support (English primary)
- Confidence scoring for extracted text
- Fallback between OCR engines

**Dependencies**:
```python
# OCR Module Dependencies
pytesseract>=0.3.10
easyocr>=1.7.0
opencv-python>=4.8.0
Pillow>=10.0.0
pdf2image>=1.16.0  # For PDF processing
```

### 2. LLM Module (`modules/llm/`)
**Purpose**: Parse unstructured text into structured invoice data

**Key Components**:
- `client.py`: Abstract LLM client interface
- `gemini_client.py`: Google Gemini API implementation
- `prompts.py`: Structured prompt templates
- `parser.py`: LLM response parsing and validation

**Features**:
- Structured JSON output extraction
- Confidence scoring for each field
- Fallback parsing for low-confidence fields
- Prompt engineering for invoice-specific extraction

**Prompt Structure**:
```python
INVOICE_EXTRACTION_PROMPT = """
Extract the following information from this invoice text in JSON format:
{
  "vendor_name": "string",
  "invoice_number": "string", 
  "invoice_date": "YYYY-MM-DD",
  "due_date": "YYYY-MM-DD",
  "items": [
    {
      "sku": "string",
      "description": "string", 
      "quantity": "number",
      "unit_price": "number",
      "total": "number"
    }
  ],
  "subtotal": "number",
  "tax": "number", 
  "total": "number"
}

Invoice text: {text}
"""
```

**Dependencies**:
```python
# LLM Module Dependencies
google-generativeai>=0.3.0
pydantic>=2.0.0
jsonschema>=4.17.0
```

### 3. Parsing Module (`modules/parsing/`)
**Purpose**: Orchestrate OCR and LLM processing, validate extracted data

**Key Components**:
- `pipeline.py`: Main parsing orchestration
- `extractors/`: Field-specific extraction logic
- `validators/`: Data validation and business rules

**Pipeline Flow**:
1. **OCR Processing**: Extract raw text from document
2. **Text Preprocessing**: Clean and structure raw text
3. **LLM Extraction**: Parse structured data using LLM
4. **Field Validation**: Validate extracted fields
5. **Business Rules**: Apply business logic (price checks, duplicates)
6. **Data Storage**: Save validated data to database

**Features**:
- Modular extractor architecture
- Configurable validation rules
- Error handling and retry logic
- Audit trail for parsing decisions

**Dependencies**:
```python
# Parsing Module Dependencies
sqlalchemy>=2.0.0
alembic>=1.11.0  # Database migrations
python-dateutil>=2.8.0
```

---

## API Endpoints

### Upload & Processing
```
POST /api/v1/upload
- Upload invoice file (PDF/image)
- Returns: upload_id, processing status

POST /api/v1/parse/{upload_id}
- Trigger parsing for uploaded file
- Returns: parsed invoice data

GET /api/v1/parse/{upload_id}/status
- Check parsing status
- Returns: status, progress, errors
```

### Dashboard & Analytics
```
GET /api/v1/dashboard/summary
- Get dashboard summary data
- Query params: date_range, vendor_id

GET /api/v1/dashboard/trends
- Get spending trends
- Query params: period, group_by

GET /api/v1/dashboard/vendors
- Get vendor summary data
- Query params: limit, date_range
```

### Alerts & Validation
```
GET /api/v1/alerts
- Get active alerts
- Query params: status, date_range

POST /api/v1/alerts/{alert_id}/resolve
- Mark alert as resolved

GET /api/v1/validation/rules
- Get validation rules configuration
```

### Export
```
GET /api/v1/export/invoices
- Export invoice data
- Query params: format (csv/pdf), filters

GET /api/v1/export/reports
- Export summary reports
- Query params: report_type, date_range
```

---

## Database Schema

### Core Tables
```sql
-- Vendors table
CREATE TABLE vendors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Invoices table
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    vendor_id INTEGER REFERENCES vendors(id),
    invoice_number VARCHAR(100) NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE,
    subtotal DECIMAL(10,2),
    tax DECIMAL(10,2),
    total DECIMAL(10,2),
    status VARCHAR(50) DEFAULT 'parsed',
    confidence_score DECIMAL(3,2),
    raw_text TEXT,
    parsed_data JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Invoice items table
CREATE TABLE invoice_items (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id),
    sku VARCHAR(100),
    description TEXT,
    quantity DECIMAL(10,2),
    unit_price DECIMAL(10,2),
    total DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Alerts table
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id),
    alert_type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    severity VARCHAR(20) DEFAULT 'medium',
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP
);
```

---

## Security & Performance Considerations

### Security
- File upload validation (type, size, content)
- API rate limiting
- JWT authentication for API access
- Input sanitization for LLM prompts
- Audit logging for all operations

### Performance
- Async processing for OCR/LLM operations
- Database indexing on frequently queried fields
- Caching for dashboard data
- File storage optimization (compression, cleanup)
- Connection pooling for database

### Monitoring
- Application performance monitoring (APM)
- Error tracking and alerting
- Processing pipeline metrics
- User activity analytics

---

## Development & Deployment

### Development Setup
```bash
# Frontend
cd frontend
npm install
npm run dev

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Environment Variables
```bash
# Backend (.env)
DATABASE_URL=postgresql://user:pass@localhost/bevscan
GEMINI_API_KEY=your_gemini_api_key
JWT_SECRET=your_jwt_secret
UPLOAD_DIR=/path/to/uploads
LOG_LEVEL=INFO

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_NAME=BevScan
```

### Docker Deployment
```dockerfile
# Backend Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## MVP Success Metrics
- **Accuracy**: >90% field extraction accuracy
- **Performance**: <30 seconds end-to-end processing
- **Reliability**: <5% processing failures
- **User Experience**: <3 clicks to upload and view results

---

## Future Enhancements (Post-MVP)
- Email integration for automatic invoice ingestion
- Advanced analytics and forecasting
- Vendor portal for invoice submission
- Mobile app for field teams
- Integration with accounting systems
- Multi-language invoice support
