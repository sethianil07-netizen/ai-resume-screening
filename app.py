"""
AI Resume Screening System
Streamlit app - matches uploaded resumes against a job description
using TF-IDF + cosine similarity, and highlights matched/missing skills.
"""

import streamlit as st
from src.pdf_parser import extract_text_from_pdf
from src.text_processing import clean_text
from src.matcher import rank_resumes
from src.skill_extractor import extract_skills_from_jd, match_skills

# ----------------------------
# Page config + light styling
# ----------------------------
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide",
)

st.markdown("""
<style>
.main-header {
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0;
}
.sub-header {
    color: #6b7280;
    font-size: 1rem;
    margin-top: 0.2rem;
    margin-bottom: 1.5rem;
}
.candidate-card {
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    background-color: #fafafa;
}
.score-badge {
    font-size: 1.6rem;
    font-weight: 700;
    color: #1d4ed8;
}
.rank-badge {
    display: inline-block;
    background-color: #1d4ed8;
    color: white;
    border-radius: 6px;
    padding: 0.15rem 0.6rem;
    font-weight: 600;
    font-size: 0.85rem;
    margin-right: 0.5rem;
}
.skill-tag-matched {
    display: inline-block;
    background-color: #dcfce7;
    color: #166534;
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    margin: 0.2rem 0.3rem 0.2rem 0;
    font-size: 0.85rem;
}
.skill-tag-missing {
    display: inline-block;
    background-color: #fee2e2;
    color: #991b1b;
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    margin: 0.2rem 0.3rem 0.2rem 0;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Session state init
# ----------------------------
if "results" not in st.session_state:
    st.session_state.results = None
if "errors" not in st.session_state:
    st.session_state.errors = []

# ----------------------------
# Header
# ----------------------------
st.markdown('<p class="main-header">📄 AI Resume Screening System</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Upload resumes and a job description to get a '
    'transparent, text-similarity based Job Match Score — not a hiring '
    'recommendation.</p>',
    unsafe_allow_html=True,
)

# ----------------------------
# Input section
# ----------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=250,
        placeholder="e.g. We are looking for a customer service representative...",
    )

with col2:
    st.subheader("2. Upload Resumes")
    uploaded_files = st.file_uploader(
        "Upload one or more PDF resumes",
        type=["pdf"],
        accept_multiple_files=True,
    )

st.markdown("---")

analyze_col, reset_col = st.columns([1, 1])
with analyze_col:
    analyze_clicked = st.button("🔍 Analyze Resumes", type="primary", use_container_width=True)
with reset_col:
    reset_clicked = st.button("↺ Reset", use_container_width=True)

if reset_clicked:
    st.session_state.results = None
    st.session_state.errors = []
    st.rerun()

# ----------------------------
# Analysis logic
# ----------------------------
if analyze_clicked:
    st.session_state.errors = []

    if not job_description or not job_description.strip():
        st.error("Please paste a job description before analyzing.")
    elif not uploaded_files:
        st.error("Please upload at least one PDF resume.")
    else:
        with st.spinner("Extracting text, analyzing content, and ranking resumes..."):
            resumes_raw = []   # for skill matching (unlemmatized text)
            resumes_clean = [] # for TF-IDF matching (cleaned text)
            errors = []

            for uploaded_file in uploaded_files:
                file_bytes = uploaded_file.read()
                result = extract_text_from_pdf(file_bytes, uploaded_file.name)

                if not result["success"]:
                    errors.append(f"{uploaded_file.name}: {result['error']}")
                    continue

                resumes_raw.append({"filename": result["filename"], "text": result["text"]})
                resumes_clean.append({
                    "filename": result["filename"],
                    "text": clean_text(result["text"]),
                })

            st.session_state.errors = errors

            if not resumes_clean:
                st.session_state.results = None
            else:
                jd_clean = clean_text(job_description)
                rankings = rank_resumes(jd_clean, resumes_clean)

                jd_skills = extract_skills_from_jd(job_description)

                # Build a lookup of raw text by filename for skill matching
                raw_lookup = {r["filename"]: r["text"] for r in resumes_raw}

                full_results = []
                for r in rankings:
                    raw_text = raw_lookup.get(r["filename"], "")
                    skill_result = match_skills(jd_skills, raw_text)
                    full_results.append({
                        **r,
                        "matched_skills": skill_result["matched"],
                        "missing_skills": skill_result["missing"],
                    })

                st.session_state.results = full_results

# ----------------------------
# Error display (per-file issues)
# ----------------------------
if st.session_state.errors:
    for err in st.session_state.errors:
        st.warning(f"⚠️ Skipped a file — {err}")

# ----------------------------
# Results display
# ----------------------------
if st.session_state.results:
    st.markdown("---")
    st.subheader(f"Ranked Results ({len(st.session_state.results)} resume(s))")

    for r in st.session_state.results:
        with st.container():
            st.markdown('<div class="candidate-card">', unsafe_allow_html=True)

            top_col, score_col = st.columns([3, 1])
            with top_col:
                st.markdown(
                    f'<span class="rank-badge">#{r["rank"]}</span>'
                    f'<strong>{r["filename"]}</strong>',
                    unsafe_allow_html=True,
                )
            with score_col:
                st.markdown(
                    f'<span class="score-badge">{r["score"]}%</span>',
                    unsafe_allow_html=True,
                )

            st.progress(min(r["score"] / 100, 1.0))

            with st.expander("View skill details"):
                st.markdown("**✅ Matched Skills**")
                if r["matched_skills"]:
                    tags = "".join(
                        f'<span class="skill-tag-matched">{s}</span>'
                        for s in r["matched_skills"]
                    )
                    st.markdown(tags, unsafe_allow_html=True)
                else:
                    st.write("No direct skill matches found.")

                st.markdown("**❌ Missing Skills**")
                if r["missing_skills"]:
                    tags = "".join(
                        f'<span class="skill-tag-missing">{s}</span>'
                        for s in r["missing_skills"]
                    )
                    st.markdown(tags, unsafe_allow_html=True)
                else:
                    st.write("No missing skills detected.")

                st.caption(
                    "Score reflects textual similarity (TF-IDF + cosine similarity) "
                    "between the resume and job description. Skills are identified "
                    "via keyword/phrase matching, not deep semantic understanding. "
                    "This is a similarity score, not a hiring recommendation."
                )

            st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.results is None and not analyze_clicked:
    st.info("👆 Paste a job description and upload resumes, then click **Analyze Resumes** to get started.")