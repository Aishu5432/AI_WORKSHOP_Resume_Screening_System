import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from resume_parser import extract_text
from rag import create_vector_store

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# SESSION VARIABLES

if "resume_data" not in st.session_state:
    st.session_state["resume_data"] = ""

if "candidate_result" not in st.session_state:
    st.session_state["candidate_result"] = ""

if "qa_result" not in st.session_state:
    st.session_state["qa_result"] = ""

if "resume_count" not in st.session_state:
    st.session_state["resume_count"] = 0

# PAGE CONFIG

st.set_page_config(
    page_title="AI Resume Screening System",
    layout="wide"
)

# CUSTOM CSS

st.markdown("""
<style>

/* ── Page background: deep navy-to-slate ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(145deg, #0f1b2d 0%, #1a2a42 50%, #162035 100%);
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stMain"] { padding-top: 2rem; background: transparent; }
section[data-testid="stMain"] > div {
    max-width: 860px;
    margin: 0 auto;
}

/* ── Sidebar (if ever used) ── */
[data-testid="stSidebar"] { background: #0d1624 !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Cards: frosted glass on dark bg ── */
.rs-card {
    background: rgba(255,255,255,0.05);
    border: 0.5px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 1.5rem 1.7rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(8px);
}

/* ── Header card: accent top border ── */
.rs-header-card {
    background: rgba(255,255,255,0.06);
    border: 0.5px solid rgba(255,255,255,0.12);
    border-top: 2.5px solid #4A8FE8;
    border-radius: 16px;
    padding: 1.5rem 1.7rem;
    margin-bottom: 1.2rem;
}
.rs-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 0.4rem;
}
.rs-header-icon {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    background: rgba(74,143,232,0.18);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    border: 0.5px solid rgba(74,143,232,0.30);
}
.rs-title {
    font-size: 1.45rem;
    font-weight: 700;
    color: #f0f4ff;
    margin: 0;
    letter-spacing: -0.02em;
}
.rs-subtitle {
    font-size: 0.85rem;
    color: rgba(200,215,240,0.65);
    margin: 3px 0 0;
}

/* ── Badges ── */
.rs-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 1rem 0 0.25rem;
}
.rs-badge {
    font-size: 12px;
    font-weight: 500;
    padding: 4px 11px;
    border-radius: 8px;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}
.rs-badge-blue   { background: rgba(74,143,232,0.18); color: #7BB8F8; border: 0.5px solid rgba(74,143,232,0.30); }
.rs-badge-green  { background: rgba(52,199,128,0.15); color: #5DD9A0; border: 0.5px solid rgba(52,199,128,0.25); }
.rs-badge-amber  { background: rgba(240,180,60,0.15);  color: #F0C84A; border: 0.5px solid rgba(240,180,60,0.25); }
.rs-badge-purple { background: rgba(150,100,240,0.15); color: #C09CF8; border: 0.5px solid rgba(150,100,240,0.25); }

/* ── Section / card labels ── */
.rs-section-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: rgba(180,200,240,0.50);
    margin-bottom: 0.6rem;
}
.rs-card-title {
    font-size: 15px;
    font-weight: 600;
    color: #e2eaff;
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    gap: 7px;
}

/* ── Upload zone ── */
.rs-upload-zone {
    border: 1.5px dashed rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 1.8rem 1rem;
    text-align: center;
    background: rgba(255,255,255,0.03);
}
.rs-upload-zone .zone-icon { font-size: 2rem; display: block; margin-bottom: 8px; }
.rs-upload-zone p { font-size: 13.5px; color: rgba(200,215,240,0.70); margin: 0 0 4px; }
.rs-upload-zone span { font-size: 12px; color: rgba(180,200,240,0.40); }
.rs-upload-zone code {
    background: rgba(255,255,255,0.08);
    color: #7BB8F8;
    padding: 1px 6px;
    border-radius: 5px;
    font-size: 12px;
}

/* ── Result box ── */
.rs-result-box {
    background: rgba(255,255,255,0.04);
    border: 0.5px solid rgba(255,255,255,0.09);
    border-left: 3px solid #4A8FE8;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    font-size: 14px;
    color: rgba(220,230,255,0.85);
    line-height: 1.80;
    margin-top: 0.75rem;
}

/* ── Streamlit buttons ── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 0.45rem 1.2rem !important;
    border: 0.5px solid rgba(255,255,255,0.18) !important;
    background: rgba(255,255,255,0.07) !important;
    color: #d8e8ff !important;
    transition: background 0.15s !important;
}
.stButton > button:hover {
    background: rgba(255,255,255,0.13) !important;
    border-color: rgba(255,255,255,0.28) !important;
}
.stButton > button[kind="primary"] {
    background: #2563B0 !important;
    color: #fff !important;
    border-color: transparent !important;
    box-shadow: 0 2px 10px rgba(37,99,176,0.40) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #1d50a0 !important;
}

/* ── Streamlit text area / input ── */
.stTextArea textarea, .stTextInput input {
    border-radius: 10px !important;
    border: 0.5px solid rgba(255,255,255,0.12) !important;
    background: rgba(255,255,255,0.05) !important;
    font-size: 14px !important;
    color: #e2eaff !important;
    caret-color: #7BB8F8 !important;
}
.stTextArea textarea::placeholder, .stTextInput input::placeholder {
    color: rgba(180,200,240,0.35) !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #4A8FE8 !important;
    box-shadow: 0 0 0 2px rgba(74,143,232,0.20) !important;
}

/* ── Streamlit metric ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border: 0.5px solid rgba(255,255,255,0.09);
    border-radius: 12px;
    padding: 0.85rem 1rem;
}
[data-testid="stMetricLabel"] { font-size: 12px !important; color: rgba(180,200,240,0.55) !important; }
[data-testid="stMetricValue"] { font-size: 20px !important; font-weight: 600 !important; color: #e2eaff !important; }

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-size: 14px !important;
    background: rgba(255,255,255,0.05) !important;
    border: 0.5px solid rgba(255,255,255,0.10) !important;
    color: #d8e8ff !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px dashed rgba(255,255,255,0.13) !important;
    border-radius: 12px !important;
    padding: 0.5rem !important;
}
[data-testid="stFileUploader"] section {
    background: transparent !important;
    border: none !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"] label {
    color: rgba(200,215,240,0.70) !important;
    font-size: 14px !important;
}
[data-testid="stFileUploader"] button {
    border-radius: 8px !important;
    background: rgba(74,143,232,0.15) !important;
    border: 0.5px solid rgba(74,143,232,0.35) !important;
    color: #7BB8F8 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
[data-testid="stFileUploader"] button:hover {
    background: rgba(74,143,232,0.25) !important;
}
[data-testid="stFileUploaderFile"] {
    background: rgba(255,255,255,0.05) !important;
    border: 0.5px solid rgba(255,255,255,0.10) !important;
    border-radius: 8px !important;
    color: #d8e8ff !important;
}
[data-testid="stFileUploaderFileName"] {
    color: #d8e8ff !important;
    font-size: 13px !important;
}
[data-testid="stFileUploaderFileData"] {
    color: rgba(180,200,240,0.50) !important;
    font-size: 12px !important;
}

/* ── Divider ── */
hr {
    border-color: rgba(255,255,255,0.07) !important;
    margin: 1.5rem 0 !important;
}

</style>
""", unsafe_allow_html=True)

# HEADER

st.markdown("""
<div class="rs-header-card">
  <div class="rs-header">
    <div class="rs-header-icon">🤖</div>
    <div>
      <p class="rs-title">AI Resume Screening System</p>
      <p class="rs-subtitle">Upload resumes, match candidates and ask questions.</p>
    </div>
  </div>
  <div class="rs-badges">
    <span class="rs-badge rs-badge-blue">⛓ LangChain</span>
    <span class="rs-badge rs-badge-green">🗄 ChromaDB</span>
    <span class="rs-badge rs-badge-amber">✨ Gemini AI</span>
    <span class="rs-badge rs-badge-purple">🔀 RAG Architecture</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# LOAD RESUMES

st.markdown('<div class="rs-card-title">📂 Resume database</div>', unsafe_allow_html=True)
st.markdown('<p class="rs-section-label">Upload .docx resume files from your browser</p>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    label="Upload Resumes",
    label_visibility="collapsed",
    type=["docx"],
    accept_multiple_files=True
)

# Save uploaded files to the resumes/ folder
if uploaded_files:

    os.makedirs("resumes", exist_ok=True)

    saved_names = []

    for uf in uploaded_files:

        save_path = os.path.join("resumes", uf.name)

        with open(save_path, "wb") as f:
            f.write(uf.getbuffer())

        saved_names.append(uf.name)

    st.markdown(
        f'<p style="font-size:13px; color: rgba(200,215,240,0.60); margin: 0.4rem 0 0;">'
        f'📎 {len(saved_names)} file(s) ready: {", ".join(saved_names)}</p>',
        unsafe_allow_html=True
    )

if st.button("⬆ Load Resumes", type="primary"):

    resume_data = ""
    texts = []
    count = 0

    try:

        if not os.path.exists("resumes") or not os.listdir("resumes"):
            st.warning("⚠ No resumes found. Please upload .docx files above first.")
        else:

            for file in os.listdir("resumes"):

                if file.endswith(".docx"):

                    path = os.path.join("resumes", file)
                    text = extract_text(path)
                    text = text[:1000]
                    resume_data += f"\n\nResume File: {file}\n"
                    resume_data += text
                    texts.append(text)
                    count += 1

            if count == 0:
                st.warning("⚠ No .docx files found in the resumes folder.")
            else:
                st.session_state["resume_data"] = resume_data
                st.session_state["resume_count"] = count

                create_vector_store(texts)

                st.success(f"✅ {count} resume(s) loaded and stored in ChromaDB")

    except Exception as e:
        st.error(f"Error loading resumes: {e}")

if st.session_state["resume_count"] > 0:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Resumes Loaded", st.session_state["resume_count"])
    with col2:
        st.metric("Vector Store", "ChromaDB")
    with col3:
        st.metric("Architecture", "RAG")

st.divider()

# JOB DESCRIPTION

st.markdown('<div class="rs-card-title">📄 Job description</div>', unsafe_allow_html=True)
st.markdown('<p class="rs-section-label">Paste the full job description below</p>', unsafe_allow_html=True)

jd = st.text_area(
    label="Job Description",
    label_visibility="collapsed",
    placeholder="e.g. We are looking for a Senior Python Developer with 5+ years of experience in FastAPI, PostgreSQL, and cloud deployments...",
    height=180
)

# MATCH CANDIDATES

if st.button("🎯 Match Candidates", type="primary"):

    if st.session_state["resume_data"] == "":
        st.warning("⚠ Please load resumes first.")
    else:

        prompt = f"""
You are an HR recruiter.

Job Description:

{jd}

Candidate Resumes:

{st.session_state["resume_data"]}

Analyze all candidates.

For each candidate provide:

1. Candidate Name
2. Match Percentage
3. Matching Skills
4. Missing Skills
5. Reason

Finally provide:

Top 3 Candidates
Best Candidate
Why they are selected
"""

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.session_state["candidate_result"] = response.text

        except Exception as e:

            if "429" in str(e):
                st.warning("⚠ Gemini quota reached. Please wait 10 seconds and try again.")
            else:
                st.error(f"Gemini error: {e}")

# SHOW MATCHING RESULT

if st.session_state["candidate_result"]:

    st.markdown('<div class="rs-card-title">🏆 Candidate ranking</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="rs-result-box">{st.session_state["candidate_result"]}</div>',
        unsafe_allow_html=True
    )

st.divider()

# QUESTION ANSWERING

st.markdown('<div class="rs-card-title">💬 Ask questions about candidates</div>', unsafe_allow_html=True)
st.markdown('<p class="rs-section-label">Answers are sourced only from the loaded resumes</p>', unsafe_allow_html=True)

question = st.text_input(
    label="Question",
    label_visibility="collapsed",
    placeholder="e.g. Which candidate has experience with Docker and Kubernetes?"
)

if st.button("🤖 Get Answer", type="primary"):

    if st.session_state["resume_data"] == "":
        st.warning("⚠ Please load resumes first.")
    else:

        prompt = f"""
Candidate Resumes:

{st.session_state["resume_data"]}

Question:

{question}

Answer ONLY using information from resumes.
"""

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.session_state["qa_result"] = response.text

        except Exception as e:

            if "429" in str(e):
                st.warning("⚠ Gemini quota reached. Please wait 10 seconds and try again.")
            else:
                st.error(f"Gemini error: {e}")

# SHOW QA RESULT

if st.session_state["qa_result"]:

    st.markdown('<div class="rs-card-title">📝 Answer</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="rs-result-box">{st.session_state["qa_result"]}</div>',
        unsafe_allow_html=True
    )
