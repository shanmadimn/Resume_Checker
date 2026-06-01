import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/analyze"

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

        files = {
            "resume": (
                uploaded_resume.name,
                uploaded_resume.getvalue(),
                "application/pdf"
            )
        }

        data = {
            "jd": jd
        }

        response = requests.post(
            API_URL,
            files=files,
            data=data
        )

        result = response.json()

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
            cols[idx % 3].success(skill)
            skill.replace("-", " ").title()
    else:
        st.info("No matched skills found.")

    st.subheader("❌ Missing Skills")

    missing_skills = result["missing_skills"]

    if missing_skills:
        cols = st.columns(3)

        for idx, skill in enumerate(missing_skills):
            cols[idx % 3].error(skill)
            skill.replace("-", " ").title()
    else:
        st.success("No missing skills detected.")

    st.subheader("🤖 AI Recruiter Feedback")

    st.markdown(result["ai_feedback"])
