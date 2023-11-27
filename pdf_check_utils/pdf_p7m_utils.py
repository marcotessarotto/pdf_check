import subprocess
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs7


def sign_pdf(pdf_path, certificate_path, private_key_path, output_path):
    # Command to digitally sign the PDF
    command = [
        'openssl', 'smime', '-sign', '-nodetach', '-binary',
        '-outform', 'DER',
        '-signer', certificate_path,
        '-inkey', private_key_path,
        '-out', output_path,
        '-in', pdf_path
    ]

    # Execute the command
    subprocess.run(command, check=True)

# # Paths to your files
# pdf_path = '/mnt/data/test.pdf'
# certificate_path = '/mnt/data/certificate.pem'
# private_key_path = '/mnt/data/key.pem'
# output_path = '/mnt/data/test.pdf.p7m'
#
# # Sign the PDF
# sign_pdf(pdf_path, certificate_path, private_key_path, output_path)



def extract_pdf_from_p7m(p7m_path, output_pdf_path):
    """
    Extract a PDF file from a PKCS#7 file.

    requires openssl to be installed and in the PATH
    :param p7m_path:
    :param output_pdf_path:
    :return:
    """
    try:
        subprocess.run(["openssl", "smime", "-decrypt", "-in", p7m_path,
                        "-inform", "DER", "-noverify", "-out", output_pdf_path],
                       check=True)
        return "Extraction successful"
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"

    # openssl smime -decrypt -in yourfile.pdf.p7m -inform DER -noverify -out extractedfile.pdf

# # Example usage
# result = extract_pdf_from_p7m("path_to_your_file.pdf.p7m", "path_to_extracted_pdf.pdf")
# print(result)


def is_openssl_installed():
    try:
        # Attempt to run 'openssl version' command
        result = subprocess.run(["openssl", "version"], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, None
    except FileNotFoundError:
        # OpenSSL is not installed or not found in PATH
        return False, None


# Example usage
installed, version = is_openssl_installed()
if installed:
    print(f"OpenSSL is installed. Version: {version}")
else:
    print("OpenSSL is not installed.")


def load_pkcs7_data(file_path):
    try:
        with open(file_path, 'rb') as file:
            pkcs7_data = file.read()

        # Load the PKCS#7 data
        p7 = pkcs7.load_pem_pkcs7_certificates(pkcs7_data, default_backend())
        # or for DER format, use: pkcs7.load_der_pkcs7_certificates(pkcs7_data, default_backend())

        return p7
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def load_pkcs7_data2(file_path):
    try:
        with open(file_path, 'rb') as file:
            pkcs7_data = file.read()

        # Check for PEM format
        if pkcs7_data.startswith(b'-----BEGIN'):
            p7 = pkcs7.load_pem_pkcs7_certificates(pkcs7_data, default_backend())
        else:
            p7 = pkcs7.load_der_pkcs7_certificates(pkcs7_data, default_backend())

        return p7
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def load_pkcs7_data3(file_path):
    try:
        with open(file_path, 'rb') as file:
            pkcs7_data = file.read()

        # Try loading in PEM format
        try:
            p7 = serialization.pkcs7.load_pem_pkcs7_certificates(pkcs7_data, default_backend())
            return p7, 'PEM'
        except ValueError:
            # If PEM loading fails, try DER
            pass

        # Try loading in DER format
        try:
            p7 = serialization.pkcs7.load_der_pkcs7_certificates(pkcs7_data, default_backend())
            return p7, 'DER'
        except ValueError:
            # If DER loading also fails
            pass

        # If both PEM and DER loading fail
        raise ValueError("The file is neither in PEM nor DER format.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

# # Example usage
# p7 = load_pkcs7_data('path_to_your_file.p7m')
# if p7:
#     print("PKCS#7 data loaded successfully.")
# else:
#     print("Failed to load PKCS#7 data.")



# # Example usage
# p7 = load_pkcs7_data('path_to_your_file.p7m')
# if p7:
#     print("PKCS#7 data loaded successfully.")
# else:
#     print("Failed to load PKCS#7 data.")
