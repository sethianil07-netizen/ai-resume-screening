# AI Resume Screening System

An AI-powered resume screening tool that matches uploaded resumes against a job description using NLP-based text similarity, and highlights which skills each candidate does and doesn't demonstrate.

Built as Task 04 for an AI Internship, focused on demonstrating real-world NLP similarity matching in a hiring-adjacent context.

> **Note:** This tool produces a *textual similarity score*, not a hiring recommendation or prediction. It is meant to assist human screening, not replace it.

---

## What It Does

1. Accepts a pasted job description
2. Accepts multiple uploaded PDF resumes
3. Extracts and cleans text from each resume
4. Computes a **Job Match Score** for each resume based on textual similarity to the job description
5. Identifies which skills from the job description appear in each resume, and which are missing
6. Displays ranked, expandable results with scores, progress bars, and skill breakdowns

---

## How It Works

The pipeline runs in five stages:

PDF Upload → Text Extraction → Text Preprocessing → TF-IDF + Cosine Similarity → Ranked Results
↘ Skill Extraction & Matching ↗


1. **Text extraction** (`pdf_parser.py`) — PyMuPDF extracts raw text from each PDF. Files that fail to extract (e.g. scanned/image-only PDFs) are skipped with a clear error message rather than crashing the app.
2. **Preprocessing** (`text_processing.py`) — Text is lowercased, stripped of noise characters, and lemmatized with spaCy (reducing words to their base form, e.g. "managing" → "manage"), with stopwords removed.
3. **Matching** (`matcher.py`) — The job description and all resumes are vectorized together using TF-IDF (Term Frequency–Inverse Document Frequency), then compared using cosine similarity to produce a 0–100% Job Match Score per resume.
4. **Skill extraction** (`skill_extractor.py`) — Candidate skill phrases are extracted from the job description using spaCy noun-chunk parsing plus a supplementary list of common skills/tools. Each resume's raw text is then checked for these phrases to produce **matched** and **missing** skill lists.
5. **UI** (`app.py`) — Streamlit ties everything together: input forms, a loading state, and ranked result cards with expandable skill details.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI |
| PyMuPDF (`pymupdf`) | PDF text extraction |
| spaCy | Text cleaning, lemmatization, noun-chunk skill extraction |
| scikit-learn | TF-IDF vectorization + cosine similarity |
| pandas | Used for internal data organization |

---

## NLP Methodology

- **Vectorization:** TF-IDF was chosen over more complex embedding-based approaches for this first version because it is transparent and explainable — every score can be traced back to actual shared vocabulary between the resume and job description, rather than an opaque neural similarity.
- **Similarity metric:** Cosine similarity measures the angle between the job description's TF-IDF vector and each resume's vector, producing a normalized similarity score independent of document length.
- **Skill extraction:** Skills are identified via noun-chunk parsing (spaCy) plus a small supplementary keyword list — this is **keyword/phrase matching, not semantic understanding**. A resume that describes a skill using entirely different wording than the job description may not register a match, even if a human reviewer would recognize the equivalence.

The architecture keeps matching logic isolated in `matcher.py`, so a future version could swap in sentence embeddings (e.g. `sentence-transformers`) for semantic matching without changing the UI or extraction layers.

---

## Scoring Methodology

The **Job Match Score** (0–100%) reflects the textual similarity between a resume and the job description, computed via TF-IDF + cosine similarity. It is:

- **Relative**, not absolute — useful for ranking resumes against each other for the *same* job description, not as a universal quality score.
- **Vocabulary-based** — influenced by shared terminology, not by inferred qualifications, experience quality, or soft factors a human reviewer would weigh.
- **Not a hiring recommendation** — explicitly framed as a similarity metric throughout the UI.

---

## Project Structure
ai-resume-screening/
│
├── app.py # Streamlit UI and pipeline orchestration
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│ ├── init.py
│ ├── pdf_parser.py # PDF text extraction
│ ├── text_processing.py # Text cleaning/lemmatization
│ ├── matcher.py # TF-IDF + cosine similarity ranking
│ └── skill_extractor.py # Skill extraction and matching
│
└── assets/ # (reserved for future static assets)


Each module in `src/` is independently testable and has no dependency on Streamlit, so the core NLP logic can be reused or tested outside the UI.

---

## Installation

```bash
git clone <your-repo-url>
cd ai-resume-screening

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Usage

```bash
streamlit run app.py
```

Then:
1. Paste a job description into the text area.
2. Upload one or more PDF resumes.
3. Click **Analyze Resumes**.
4. Review ranked results — click **View skill details** on any candidate to see matched/missing skills.
5. Click **Reset** to clear and start over.

---

## Limitations

- **TF-IDF is vocabulary-based**, not semantic — it won't recognize that "ML" and "machine learning" refer to the same skill unless both appear.
- **Scanned/image-only PDFs** cannot be processed, since no OCR step is included in this version.
- **Skill extraction is keyword/phrase-based**, using noun-chunk parsing, which can occasionally produce imperfect phrases (e.g. merging adjacent sentence fragments) or miss skills phrased in unexpected ways.
- **Scores are relative**, not calibrated against any external benchmark — they should be read as "more/less similar," not as a percentage of qualification.
- **No persistent storage** — uploaded resumes are processed in memory only and are not saved, by design (privacy).

## Future Improvements

- Swap TF-IDF for sentence-embedding-based semantic matching (e.g. `sentence-transformers`) for better synonym/paraphrase handling
- Add OCR support for scanned resumes
- Build a curated, categorized skills taxonomy (technical vs soft skills) instead of relying solely on noun-chunk extraction
- Add exportable results (CSV/PDF report of rankings)
- Add support for comparing against multiple job descriptions at once

---

## Privacy & Security

- All processing is local — no resume content is sent to external APIs.
- Uploaded resumes are held in memory for the duration of the session only and are not written to disk or logged.