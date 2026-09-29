"""
matcher.py

Responsible for TF-IDF vectorization, cosine similarity scoring,
and ranking resumes against the job description.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def rank_resumes(job_description_clean, resumes_clean):
    """
    Rank resumes by similarity to a job description using TF-IDF + cosine similarity.

    Args:
        job_description_clean: str, cleaned job description text.
        resumes_clean: list of dicts, each with at least
            {"filename": str, "text": str} where "text" is cleaned.

    Returns:
        list of dicts, sorted by score descending:
            {"filename": str, "score": float (0-100, rounded)}
    """
    if not job_description_clean or not resumes_clean:
        return []

    # Build the corpus: JD first, then each resume, in order.
    corpus = [job_description_clean] + [r["text"] for r in resumes_clean]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Row 0 is the JD; rows 1..n are the resumes.
    jd_vector = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(jd_vector, resume_vectors)[0]

    results = []
    for resume, score in zip(resumes_clean, similarities):
        results.append({
            "filename": resume["filename"],
            "score": round(float(score) * 100, 2),
        })

    # Sort by score, highest first
        results = []
    for resume, score in zip(resumes_clean, similarities):
        results.append({
            "filename": resume["filename"],
            "score": round(float(score) * 100, 2),
        })

    # Sort by score, highest first
    results.sort(key=lambda x: x["score"], reverse=True)

    # Add rank numbers now that the list is sorted
    for i, result in enumerate(results, start=1):
        result["rank"] = i

    return results
    results.sort(key=lambda x: x["score"], reverse=True)

    return results