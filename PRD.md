Cursor Context Setup for PRD: BevScan
========================================

## Project Name:
BevScan — Smart Invoice Parser for Beverage Teams

## Description:
This tool helps beverage directors automate and manage vendor invoices by parsing them into structured data, providing cost insights, flagging discrepancies, and visualizing trends.

---

## Core Context Files to Load:
- `PRD.md` (Product Requirements Document)
- `userflows.md` (User journeys: Upload → Parse → Validate → Report)
- `tech_spec.md` (Suggested: architecture, API design, LLM strategy)
- `.cursor/rules/coding-style.mdc` (Style guide)
- `.cursor/rules/component-patterns.mdc` (Preferred folder/component structure)

---

## Cursor Rules to Add (stored as .mdc or .cursorrules)

### General:
```mdc
- Only include features listed in PRD version 1.0.
- Prioritize simplicity and readability in all code.
- Favor modular and loosely coupled components.
```

### Component Scaffolding:
```mdc
- For UI: Use Next.js or React. Folder: `/components`, `/pages`
- For backend: Use Node.js + Express or Python + FastAPI
- For document processing: Use OCR → LLM pipeline
- Store parsed invoice data in PostgreSQL (relational schema)
```

### Feature-Specific:
```mdc
- Invoice ingestion should support drag-drop + email ingestion.
- Parsing should extract: vendor name, invoice #, date, SKU, quantity, unit cost, total
- Dashboard should include time filters and top vendor/item summaries
- Alerts must fire on price changes >5% or duplicate invoice IDs
```

### UI Guidelines:
```mdc
- UI must include: upload screen, dashboard with graphs, alert panel
- Export buttons for CSV/PDF are placed in dashboard header
- Use tooltips or info-icons to explain data points
```

---

## Suggested Next Step (for AI agents like Gemini CLI or Cursor):
> "Analyze `PRD.md` and generate a technical spec with proposed components and file structure for MVP. Highlight LLM-related modules separately."

---

## MVP Scope (from PRD):
Focus only on:
- Ingestion (PDF/email)
- Parsing to structured data
- Validation (alerts)
- Dashboard with trends + CSV export

Exclude:
- POS integrations
- Real-time sync
- Demand forecasting
- Payments

---

## Assumptions to Enforce:
```mdc
- Invoices are digital-first (PDF/email preferred)
- User will correct any OCR error via UI manually
- Minimal user onboarding required
```

---

## Output Targets for Agents:
- `/pages/Upload.tsx`
- `/components/InvoiceParser.ts`
- `/api/parseInvoice.ts`
- `/components/Dashboard.tsx`
- `/utils/ocrPipeline.ts`
- `/utils/priceAlert.ts`

---

This setup helps Cursor or Gemini agents remain focused, generate clean code aligned with goals, and support a structured MVP flow without bloat or drift.

