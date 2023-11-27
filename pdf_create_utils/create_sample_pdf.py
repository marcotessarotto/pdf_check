from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import NameObject, createStringObject
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime


def create_sample_pdf(output_pdf_path):
    # Create a simple PDF file
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(100, 750, "This is a test PDF file.")
    can.drawString(100, 730, "Created for digital signature testing.")
    can.drawString(100, 710, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}")
    can.save()

    # Move the buffer position to the beginning
    packet.seek(0)

    # Create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    writer = PdfFileWriter()
    page = new_pdf.getPage(0)
    writer.addPage(page)

    # Create a placeholder for the signature
    writer.addMetadata({
        NameObject('/Title'): createStringObject('Test PDF Document'),
        NameObject('/Author'): createStringObject('pdf_check_utils'),
        NameObject('/Subject'): createStringObject('Digital Signature Test'),
    })

    # Save the PDF to a file
    # output_pdf_path = '/mnt/data/test_pdf_document.pdf'
    with open(output_pdf_path, "wb") as output:
        writer.write(output)

