from src.pdf_parser import extract_text_from_pdf
from src.skill_extractor import extract_skills_from_jd, match_skills
import os

job_description = """
We are looking for a customer service representative with experience
working with clients, maintaining records, and coordinating with
healthcare professionals. Strong communication skills and Microsoft
Office experience required.
"""

jd_skills = extract_skills_from_jd(job_description)
print("--- JD Skills ---")
print(jd_skills)

folder = "test_resumes"

for filename in os.listdir(folder):
    if filename.lower().endswith(".pdf"):
        path = os.path.join(folder, filename)
        with open(path, "rb") as f:
            file_bytes = f.read()

        result = extract_text_from_pdf(file_bytes, filename)

        if result["success"]:
            match_result = match_skills(jd_skills, result["text"])
            print(f"\n--- {filename} ---")
            print(f"Matched: {match_result['matched']}")
            print(f"Missing: {match_result['missing']}")
        else:
            print(f"\n--- {filename} ---")
            print(f"Skipped: {result['error']}")