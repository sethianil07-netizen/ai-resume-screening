"""
skill_extractor.py

Responsible for extracting a skill vocabulary from the job
description and checking which of those skills appear in each
resume (matched vs missing skills).
"""

import re
import spacy

try:
    _nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    _nlp = spacy.load("en_core_web_sm")

COMMON_SKILLS = [
    "python", "java", "javascript", "sql", "excel", "communication",
    "leadership", "teamwork", "problem solving", "project management",
    "customer service", "data analysis", "machine learning",
    "time management", "microsoft office", "git", "html", "css",
]

GENERIC_TERMS = {
    "experience", "professional", "role", "position", "job",
    "candidate", "requirement", "requirements", "team", "work",
    "opportunity", "years",
}


def extract_skills_from_jd(jd_raw_text):
    if not jd_raw_text:
        return []

    normalized = re.sub(r"\s+", " ", jd_raw_text).strip()
    doc = _nlp(normalized.lower())
    skills = set()

    for chunk in doc.noun_chunks:
        tokens = [t.text for t in chunk if not t.is_stop and not t.is_punct]
        phrase = " ".join(tokens).strip()

        if not phrase:
            continue
        if phrase in GENERIC_TERMS:
            continue
        if len(phrase) < 2 or len(phrase) > 40:
            continue
        if phrase.isdigit():
            continue

        skills.add(phrase)

    jd_lower = normalized.lower()
    for skill in COMMON_SKILLS:
        if skill in jd_lower:
            skills.add(skill)

    return sorted(skills)


def match_skills(jd_skills, resume_raw_text):
    resume_normalized = re.sub(r"\s+", " ", resume_raw_text or "").strip()
    resume_lower = resume_normalized.lower()

    matched = []
    missing = []

    for skill in jd_skills:
        if skill in resume_lower:
            matched.append(skill)
        else:
            missing.append(skill)

    return {"matched": matched, "missing": missing}