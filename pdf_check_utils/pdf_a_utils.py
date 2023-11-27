import PyPDF2

def is_pdf_a(file_path):
    try:
        # Open the PDF file
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)

            # Accessing the document info
            doc_info = reader.getDocumentInfo()
            xmp_metadata = reader.getXmpMetadata()

            # Checking for PDF/A compliance in metadata
            if xmp_metadata and xmp_metadata.dc_format == 'application/pdf':
                if 'pdfaid' in xmp_metadata.custom_properties:
                    pdfa_info = xmp_metadata.custom_properties['pdfaid']
                    if pdfa_info.get('part') and pdfa_info.get('conformance'):
                        return True
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


# # Example usage
# pdf_file = 'path_to_your_pdf.pdf' # Replace with your PDF file path
# if is_pdf_a(pdf_file):
#     print(f"{pdf_file} is a PDF/A format.")
# else:
#     print(f"{pdf_file} is not a PDF/A format.")
