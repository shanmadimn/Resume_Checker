import pdfplumber
from io import BytesIO
import re
from groq import Groq
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_data
def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from uploaded PDF.
    """

    text_parts = []

    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text_parts.append(page_text)

    return "\n".join(text_parts).strip()

SKILLS = {
    "Programming": [
        "python",
        "java",
        "c++",
        "javascript",
        "typescript"
    ],

    "AI_ML": [
        "machine learning",
        "deep learning",
        "nlp",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "llm",
        "langchain",
        "rag"
    ],

    "Backend": [
        "fastapi",
        "flask",
        "django",
        "rest api"
    ],

    "Cloud": [
        "aws",
        "docker",
        "kubernetes"
    ],

    "Database": [
        "mysql",
        "postgresql",
        "mongodb"
    ]
}

ALL_SKILLS = {
    skill.lower()
    for category in SKILLS.values()
    for skill in category
}

@st.cache_resource
def load_model():
    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

def semantic_similarity(
    resume_text: str,
    jd_text: str
) -> float:

    model = load_model()

    embeddings = model.encode(
    [resume_text, jd_text],
    convert_to_numpy=True
    )

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(score)

def normalize(text: str) -> str:

    text = text.lower()

    def normalize(text: str) -> str:

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9\+\-\#\s]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

    return text.strip()

    return text


def extract_skills(text: str):

    text = normalize(text)

    found = []

    for skill in ALL_SKILLS:

        if re.search(
            rf"\b{re.escape(skill)}\b",
            text
        ):
            found.append(skill)

    return sorted(list(set(found)))


def skill_gap_analysis(
    resume_text: str,
    jd_text: str
):

    resume_skills = set(
        extract_skills(resume_text)
    )

    jd_skills = set(
        extract_skills(jd_text)
    )

    matched = list(
        resume_skills.intersection(jd_skills)
    )

    missing = list(
        jd_skills - resume_skills
    )

    return matched, missing


def ats_score(
    semantic_score,
    skill_score
):

    score = (
        semantic_score * 0.6 +
        skill_score * 0.4
    )

    return round(score * 100, 2)


def analyze_resume(
    resume_text,
    jd_text
):

    semantic_score = semantic_similarity(
        resume_text,
        jd_text
    )

    matched, missing = skill_gap_analysis(
        resume_text,
        jd_text
    )

    total_jd_skills = len(
        extract_skills(jd_text)
    )

    skill_score = 0

    if total_jd_skills > 0:

        skill_score = (
            len(matched) /
            total_jd_skills
        )

    final_score = ats_score(
        semantic_score,
        skill_score
    )

    return {
    "semantic_score": round(
        semantic_score * 100,
        2
    ),

    "ats_score": final_score,

    "matched_skills": matched,

    "missing_skills": missing
}

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

def generate_feedback(
    resume_text: str,
    jd_text: str,
    matched_skills: list,
    missing_skills: list,
    ats_score: float
):

    try:

        prompt = f"""
            You are an expert technical recruiter.

            Analyze the candidate's resume against the job description.

            ATS Score:
            {ats_score}

            Matched Skills:
            {matched_skills}

            Missing Skills:
            {missing_skills}

            Resume:
            {resume_text[:5000]}

            Job Description:
            {jd_text[:3000]}

            Return:

            Strengths:
    
            Weaknesses:
        
            Recommendations:
        
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=700
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"AI feedback unavailable: {str(e)}"

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")

uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

jd = st.text_area(
    "Paste Job Description",
    height=250
)

if st.button("Analyze Resume"):

    if uploaded_resume is None:
        st.error("Upload a resume.")
        st.stop()

    if not jd:
        st.error("Enter a job description.")
        st.stop()

    with st.spinner("Analyzing..."):
        resume_text = extract_text_from_pdf(
        uploaded_resume.getvalue()
        )

        result = analyze_resume(
            resume_text,
            jd
        )

        feedback = generate_feedback(
            resume_text=resume_text,
            jd_text=jd,
            matched_skills=result["matched_skills"],
            missing_skills=result["missing_skills"],
            ats_score=result["ats_score"]
        )

        result["ai_feedback"] = feedback

    st.success("Analysis Complete")

    ats = result["ats_score"]

    if ats >= 80:
        st.success("Excellent ATS Match")
    elif ats >= 60:
        st.warning("Moderate ATS Match")
    else:
        st.error("Low ATS Match")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "ATS Score",
            f"{ats}%"
        )

    with col2:
        st.metric(
            "Semantic Match",
            f"{result['semantic_score']}%"
        )

    st.subheader("✅ Matched Skills")

    matched_skills = result["matched_skills"]

    if matched_skills:
        cols = st.columns(3)

        for idx, skill in enumerate(matched_skills):
            formatted_skill = (
            skill.replace("-", " ")
            .title()
            )

            cols[idx % 3].success(
            formatted_skill
        )
    else:
        st.info("No matched skills found.")

    st.subheader("❌ Missing Skills")

    missing_skills = result["missing_skills"]

    if missing_skills:
        cols = st.columns(3)

        for idx, skill in enumerate(missing_skills):
            formatted_skill = (
            skill.replace("-", " ")
            .title()
            )
            cols[idx % 3].error(formatted_skill)
    else:
        st.success("No missing skills detected.")

    st.subheader("🤖 AI Recruiter Feedback")

    st.markdown(result["ai_feedback"])
