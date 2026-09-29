from src.pdf_parser import extract_text_from_pdf
import os

folder = "test_resumes"

for filename in os.listdir(folder):
    if filename.lower().endswith(".pdf"):
        path = os.path.join(folder, filename)
        with open(path, "rb") as f:
            file_bytes = f.read()

        result = extract_text_from_pdf(file_bytes, filename)

        print(f"\n--- {result['filename']} ---")
        print(f"Success: {result['success']}")
        if result["success"]:
            print(f"Extracted {len(result['text'])} characters")
            print(result["text"][:300])  # preview first 300 chars
        else:
            print(f"Error: {result['error']}")