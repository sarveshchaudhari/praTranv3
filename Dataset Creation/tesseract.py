import fitz  # PyMuPDF
import io
from google.cloud import vision

# Set up the Google Cloud Vision client
client = vision.ImageAnnotatorClient()

# PDF file path
pdf_path = "./gaudavaho_001364_hr.pdf"  # Replace with your PDF file
output_file = "extracted_text.txt"

# Open the PDF file
doc = fitz.open(pdf_path)

# Define the page range (PyMuPDF uses 0-based index, so page 118 is index 117)
start_page = 117  # Page 118
end_page = 588  # Page 588

with open(output_file, "w", encoding="utf-8") as file:
    for page_num in range(start_page, end_page):
        print(f"Processing page {page_num + 1}...")

        # Convert PDF page to an image
        page = doc[page_num]
        pix = page.get_pixmap()
        image_bytes = pix.tobytes("png")

        # Prepare image for OCR
        image = vision.Image(content=image_bytes)

        # Perform OCR (Text Detection)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        # Write extracted text to file
        if texts:
            extracted_text = texts[0].description
            file.write(f"\n\n===== Page {page_num + 1} =====\n")
            file.write(extracted_text)
        else:
            file.write(f"\n\n===== Page {page_num + 1} (No text detected) =====\n")

        # Error handling
        if response.error.message:
            print(f"Error on page {page_num + 1}: {response.error.message}")

print(f"Text extraction complete. Saved to {output_file}")
