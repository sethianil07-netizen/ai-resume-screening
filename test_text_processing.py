from src.pdf_parser import extract_text_from_pdf
from src.text_processing import clean_text
import os

folder = "test_resumes"

for filename in os.listdir(folder):
    if filename.lower().endswith(".pdf"):
        path = os.path.join(folder, filename)
        with open(path, "rb") as f:
            file_bytes = f.read()

        result = extract_text_from_pdf(file_bytes, filename)

        if result["success"]:
            cleaned = clean_text(result["text"])
            print(f"\n--- {result['filename']} ---")
            print(cleaned[:400])
        else:
            print(f"\n--- {result['filename']} ---")
            print(f"Skipped (extraction failed): {result['error']}")