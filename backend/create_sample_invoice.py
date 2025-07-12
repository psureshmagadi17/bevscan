#!/usr/bin/env python3
"""
Create a sample beverage industry invoice PDF for testing BevScan
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER
import os
from datetime import datetime, timedelta

def create_sample_invoice():
    """Create a sample beverage industry invoice PDF"""
    
    # Create uploads directory if it doesn't exist
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    
    # File path
    filename = os.path.join(uploads_dir, "sample_beverage_invoice.pdf")
    
    # Create PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=6
    )
    
    # Content elements
    elements = []
    
    # Title
    elements.append(Paragraph("INVOICE", title_style))
    elements.append(Spacer(1, 20))
    
    # Company header
    company_data = [
        ["Beverage Supply Co.", "INVOICE #: INV-2024-001"],
        ["123 Main Street", "DATE: " + datetime.now().strftime("%B %d, %Y")],
        ["San Francisco, CA 94102", "DUE DATE: " + (datetime.now() + timedelta(days=30)).strftime("%B %d, %Y")],
        ["Phone: (555) 123-4567", ""],
        ["Email: sales@beveragesupply.com", ""],
    ]
    
    company_table = Table(company_data, colWidths=[4*inch, 2*inch])
    company_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, 2), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(company_table)
    elements.append(Spacer(1, 20))
    
    # Bill to section
    elements.append(Paragraph("BILL TO:", header_style))
    bill_to_data = [
        ["Downtown Bar & Grill"],
        ["456 Restaurant Row"],
        ["San Francisco, CA 94103"],
        ["Phone: (555) 987-6543"],
        ["Email: manager@downtownbar.com"],
    ]
    
    bill_to_table = Table(bill_to_data, colWidths=[6*inch])
    bill_to_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(bill_to_table)
    elements.append(Spacer(1, 20))
    
    # Items table
    elements.append(Paragraph("ITEMS:", header_style))
    
    # Sample beverage items
    items_data = [
        ["ITEM", "DESCRIPTION", "QTY", "UNIT PRICE", "TOTAL"],
        ["Craft Beer", "Local IPA - 24oz Bottles", "48", "$2.50", "$120.00"],
        ["Wine", "Cabernet Sauvignon - 750ml", "24", "$8.75", "$210.00"],
        ["Spirits", "Premium Vodka - 750ml", "12", "$15.00", "$180.00"],
        ["Mixers", "Tonic Water - 12oz Cans", "72", "$0.75", "$54.00"],
        ["Garnishes", "Fresh Limes - 50 count", "2", "$12.50", "$25.00"],
    ]
    
    items_table = Table(items_data, colWidths=[1.2*inch, 2.5*inch, 0.8*inch, 1*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (4, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 20))
    
    # Totals
    totals_data = [
        ["", "", "", "SUBTOTAL:", "$589.00"],
        ["", "", "", "TAX (8.5%):", "$50.07"],
        ["", "", "", "TOTAL:", "$639.07"],
    ]
    
    totals_table = Table(totals_data, colWidths=[1.2*inch, 2.5*inch, 0.8*inch, 1*inch, 1*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (3, -1), 'RIGHT'),
        ('ALIGN', (4, 0), (4, -1), 'CENTER'),
        ('FONTNAME', (3, 0), (4, -1), 'Helvetica-Bold'),
        ('FONTNAME', (3, 2), (4, 2), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LINEABOVE', (3, 2), (4, 2), 2, colors.black),
    ]))
    elements.append(totals_table)
    elements.append(Spacer(1, 30))
    
    # Payment terms
    payment_terms = [
        "PAYMENT TERMS: Net 30 days",
        "Please make checks payable to: Beverage Supply Co.",
        "Thank you for your business!"
    ]
    
    for term in payment_terms:
        elements.append(Paragraph(term, styles['Normal']))
        elements.append(Spacer(1, 6))
    
    # Build PDF
    doc.build(elements)
    
    print(f"✅ Sample invoice created: {filename}")
    return filename

if __name__ == "__main__":
    create_sample_invoice() 