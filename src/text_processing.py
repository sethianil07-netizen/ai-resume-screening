"""
text_processing.py

Responsible for cleaning and normalizing text (both the job
description and extracted resume text) before it's vectorized.
"""

import re
import spacy

# Load the spaCy English model once, at import time,
# so we're not reloading it on every function call.
try:
    _nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    _nlp = spacy.load("en_core_web_sm")


def clean_text(raw_text):
    """
    Clean and normalize a block of text for NLP matching.

    Steps: lowercase -> remove noise characters -> collapse
    whitespace -> lemmatize -> remove stopwords.

    Args:
        raw_text: str, raw extracted text.

    Returns:
        str: cleaned, space-joined lemmatized text.
    """
    if not raw_text:
        return ""

    # Lowercase
    text = raw_text.lower()

    # Remove bullet characters, special symbols (keep letters, numbers, spaces, @ and .)
    text = re.sub(r"[^a-z0-9@.\s]", " ", text)

    # Collapse whitespace/newlines
    text = re.sub(r"\s+", " ", text).strip()

    # Lemmatize + remove stopwords using spaCy
    doc = _nlp(text)
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_space and token.lemma_.strip()
    ]

    return " ".join(tokens)