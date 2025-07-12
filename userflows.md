# Userflows — BevScan MVP

## 1. Upload Invoice
- User selects or drags a PDF/image/email invoice into the system
- System detects file type and uploads to backend
- User receives a confirmation that upload was successful

## 2. Parse Invoice
- OCR extracts raw text from document
- LLM parses vendor name, date, invoice number, line-items (SKU, quantity, unit cost, total)
- Parsed data is saved to database

## 3. Validate Data
- System checks for:
  - Price discrepancies >5% from historical data
  - Duplicate invoice IDs
- If any issues detected, an alert is triggered (email/in-app)

## 4. View Dashboard
- User opens dashboard with:
  - Time-based spend trends
  - Top vendors and top items
  - Export options for CSV and PDF

## 5. Export Reports
- User downloads filtered reports (by vendor, category, time period)
- Reports used for finance or vendor negotiation
