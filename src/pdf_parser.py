"""
pdf_parser.py

Responsible for extracting raw text from uploaded resume PDFs
using PyMuPDF (fitz).
"""

import fitz  # PyMuPDF


def extract_text_from_pdf(file_bytes, filename="unknown.pdf"):
    """
    Extract text from a PDF given as raw bytes.

    Args:
        file_bytes: the PDF file content as bytes.
        filename: original filename, used for error messages.

    Returns:
        dict with keys:
            "filename": str
            "text": str (empty string if extraction failed)
            "success": bool
            "error": str or None
    """
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as e:
        return {
            "filename": filename,
            "text": "",
            "success": False,
            "error": f"Could not open PDF: {e}",
        }

    text_parts = []
    for page in doc:
        text_parts.append(page.get_text())
    doc.close()

    full_text = "\n".join(text_parts).strip()

    if not full_text:
        return {
            "filename": filename,
            "text": "",
            "success": False,
            "error": "No extractable text found (likely a scanned/image-only PDF).",
        }

    return {
        "filename": filename,
        "text": full_text,
        "success": True,
        "error": None,
    }