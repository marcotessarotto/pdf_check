from PyPDF2 import PdfFileReader, PdfFileWriter
from datetime import datetime
import os
import subprocess


def create_self_signed_certificate(cert_path, key_path, common_name="pdf_check_utils", days_valid=365):
    """
    Creates a self-signed certificate and private key for demonstration purposes.

    Args:
    cert_path (str): Path where the certificate will be saved.
    key_path (str): Path where the private key will be saved.
    common_name (str): Common Name to be used in the certificate. Default is "pdf_check_utils".
    days_valid (int): Number of days the certificate will be valid. Default is 365.

    Returns:
    bool: True if the certificate and key were created successfully, False otherwise.
    """
    try:
        # Command to generate a self-signed certificate
        command = [
            "openssl", "req", "-x509", "-newkey", "rsa:4096",
            "-keyout", key_path,
            "-out", cert_path,
            "-days", str(days_valid),
            "-nodes",
            "-subj", f"/CN={common_name}"
        ]

        # Execute the command
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error in creating certificate: {e}")
        return False


# # Example usage of the function
# certificate_path = '/path/to/certificate.pem'  # public key
# private_key_path = '/path/to/private_key.pem'
# create_self_signed_certificate(certificate_path, private_key_path)
#
# # Path to the created PDF and where the signed PDF will be saved
# pdf_path = output_pdf_path
# signed_pdf_path = '/mnt/data/signed_test_pdf_document.pdf'
#
# # Sample self-signed certificate and private key (for demonstration purposes)
# certificate_path = '/mnt/data/certificate.pem'
# private_key_path = '/mnt/data/key.pem'


def pdf_self_sign(pdf_path, signed_pdf_path, certificate_path, private_key_path):
    """
    Digitally sign a PDF file.
    :param pdf_path: original pdf file path
    :param signed_pdf_path:  signed pdf file path
    :param certificate_path:  public key path
    :param private_key_path:  private key path
    :return:
    """
    # Create a self-signed certificate and private key for demonstration
    # !openssl req -x509 -newkey rsa:4096 -keyout {private_key_path} -out {certificate_path} -days 365 -nodes -subj "/CN=pdf_check_utils"

    # Create a self-signed certificate and private key for demonstration
    create_self_signed_certificate(certificate_path, private_key_path)

    # Prepare to sign the PDF
    with open(pdf_path, 'rb') as fp:
        reader = PdfFileReader(fp)
        writer = PdfFileWriter()

        # Copy the contents of the original PDF to the writer
        for page in range(reader.getNumPages()):
            writer.addPage(reader.getPage(page))

        # Signature metadata
        signature_metadata = {
            '/Location': 'Internet',
            '/Reason': 'Demonstration of Digital Signature',
            '/ContactInfo': 'info@example.com',
            '/Name': 'pdf_check_utils',
            '/M': datetime.now()
        }

        # Create a signature dictionary
        signature_dictionary = writer._add_signature_field(signature_metadata)

        # Metadata for the signature
        metadata = PdfSignatureMetadata(
            location='Internet',
            reason='Demonstration of Digital Signature',
            contact='info@example.com',
            signer_name='pdf_check_utils',
            signing_date=datetime.now()
        )

        # Sign the PDF
        with open(certificate_path, 'rb') as cert_fp, open(private_key_path, 'rb') as key_fp:
            writer.sign(
                output=signed_pdf_path,
                appearance_st=pdf.SignatureObject.APPEARANCE_MODES['DESCRIPTION_ONLY'],
                key=key_fp.read(),
                cert=cert_fp.read(),
                other_certs=[],
                algorithm='sha256',
                metadata=metadata
            )

    signed_pdf_path
