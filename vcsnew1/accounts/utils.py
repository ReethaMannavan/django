import os
from reportlab.pdfgen import canvas
from django.conf import settings

def generate_invoice_pdf(invoice):
    folder = os.path.join(settings.MEDIA_ROOT, "invoices")
    os.makedirs(folder, exist_ok=True)

    filename = f"{invoice.invoice_number}.pdf"
    filepath = os.path.join(folder, filename)

    c = canvas.Canvas(filepath)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "Vetri Consultancy Services")

    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Invoice Number: {invoice.invoice_number}")
    c.drawString(50, 740, f"Customer: {invoice.user.username}")
    c.drawString(50, 720, f"Plan: {invoice.plan}")
    c.drawString(50, 700, f"Amount: INR {invoice.amount}")
    c.drawString(50, 680, f"Date: {invoice.created_at.strftime('%Y-%m-%d')}")

    c.drawString(50, 640, "Thank you for choosing VCS Careers.")

    c.save()

    return f"invoices/{filename}"
