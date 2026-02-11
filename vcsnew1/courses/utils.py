# courses/utils.py
import os
from reportlab.pdfgen import canvas
from django.conf import settings

def generate_certificate(progress):
    folder = os.path.join(settings.MEDIA_ROOT, "certificates")
    os.makedirs(folder, exist_ok=True)

    filename = f"certificate_{progress.id}.pdf"
    filepath = os.path.join(folder, filename)

    c = canvas.Canvas(filepath)
    c.drawString(100, 750, "VCS Certificate of Completion")
    c.drawString(100, 700, f"Name: {progress.user.username}")
    c.drawString(100, 670, f"Course: {progress.course.title}")
    c.save()

    progress.certificate_file = f"certificates/{filename}"
    progress.save()
