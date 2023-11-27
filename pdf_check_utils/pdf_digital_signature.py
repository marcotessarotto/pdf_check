import PyPDF2
from OpenSSL import crypto
from OpenSSL.crypto import FILETYPE_ASN1, verify
from OpenSSL.crypto import X509Store, X509StoreContext, load_certificate
import os

from pdf_check_utils.pdf_p7m_utils import load_pkcs7_data


def is_pdf_signed(pdf_path):
    """Check if a PDF file is digitally signed."""
    # Open the PDF file
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        # Check each page for annotations
        for i in range(reader.numPages):
            page = reader.getPage(i)
            if '/Annots' in page:
                annotations = page['/Annots']
                for annotation in annotations:
                    annot_obj = annotation.getObject()
                    if annot_obj.get('/Subtype') == '/Widget' and annot_obj.get('/FT') == '/Sig':
                        return True
    return False

# # Example usage
# pdf_file = 'path_to_your_pdf.pdf' # Replace with your PDF file path
# if is_pdf_signed(pdf_file):
#     print("The PDF is digitally signed.")
# else:
#     print("The PDF is not digitally signed.")


def verify_p7m(p7m_file_path, cert_file_path):
    """Verify a PKCS#7 signature."""
    # Load the PKCS#7 file
    with open(p7m_file_path, 'rb') as file:
        p7m_data = file.read()

    # Load the signer's certificate
    with open(cert_file_path, 'rb') as file:
        cert_data = file.read()
    certificate = load_certificate(FILETYPE_ASN1, cert_data)

    # Create a certificate store and add the certificate
    store = X509Store()
    store.add_cert(certificate)

    # Load and verify the PKCS#7 data
    p7 = load_pkcs7_data(FILETYPE_ASN1, p7m_data)
    store_ctx = X509StoreContext(store, p7)
    try:
        store_ctx.verify_certificate()
        print("Signature is valid.")
    except Exception as e:
        print(f"Signature verification failed: {e}")

"""
Notes:

    File Formats: PKCS#7 files can be in PEM or DER format. The function above assumes PEM format; if you're working with DER, you'll need to use load_der_pkcs7_certificates instead.
    Functionality: This implementation is basic and is intended to load PKCS#7 certificate data. Depending on your needs (e.g., if you need to handle signed data, extract certificates, etc.), you might need additional functionality.
    Error Handling: Proper error handling is included, which is crucial for dealing with potential issues like file access errors or invalid data.
"""