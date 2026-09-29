from src.pdf_parser import extract_text_from_pdf
from src.text_processing import clean_text
from src.matcher import rank_resumes
import os

# A short sample job description — replace with something more realistic if you like
job_description = """
We are looking for a customer service representative with experience
working with clients, maintaining records, and coordinating with
healthcare professionals. Strong communication skills required.
"""

folder = "test_resumes"
resumes_clean = []

for filename in os.listdir(folder):
    if filename.lower().endswith(".pdf"):
        path = os.path.join(folder, filename)
        with open(path, "rb") as f:
            file_bytes = f.read()

        result = extract_text_from_pdf(file_bytes, filename)

        if result["success"]:
            cleaned = clean_text(result["text"])
            resumes_clean.append({"filename": filename, "text": cleaned})
        else:
            print(f"Skipped {filename}: {result['error']}")

jd_clean = clean_text(job_description)
rankings = rank_resumes(jd_clean, resumes_clean)

print("\n--- Rankings ---")
for r in rankings:
    print(f"{r['filename']}: {r['score']}%")