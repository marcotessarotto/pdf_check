import PyPDF2


def enumerate_pdf_structures(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Get document metadata
        metadata = reader.metadata
        print(f"Document Metadata: {metadata}")

        # Access the XMP metadata
        xmp_metadata = reader.metadata.xmp_metadata

        if xmp_metadata:
            print("XMP Metadata:")
            print(xmp_metadata)
        else:
            print("No XMP metadata found.")

        # Enumerate pages and their contents
        num_pages = len(reader.pages)
        print(f"Number of Pages: {num_pages}")

        for i in range(num_pages):
            page = reader.pages[i]
            print(f"\nPage {i+1}:")

            # Extract text
            print("Text:", page.extract_text())

            # Extract annotations
            annotations = page.get("/Annots")
            if annotations:
                print("Annotations:")
                for annot in annotations:
                    if annot.get("/Subtype") == "/Link":
                        print(" - Link Annotation:", annot.get("/A"))
                    else:
                        print(" - Other Annotation:", annot)

            # Extract images - This is more complex and might not work for all PDFs
            print("Images:")
            xObject = page.get("/Resources").get("/XObject").get_object()
            if xObject:
                for obj in xObject:
                    if xObject[obj].get("/Subtype") == "/Image":
                        print(" - Image found")


# Example usage
enumerate_pdf_structures('../workpdf/test_external.pdf')


