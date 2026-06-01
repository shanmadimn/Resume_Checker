from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
from backend.services.analyzer import analyze_resume
from backend.services.llm_feedback import (
    generate_feedback
)

from backend.schemas import (
    HealthResponse,
    AnalysisResponse
)

from backend.services.parser import (
    extract_text_from_pdf
)

from backend.services.analyzer import (
    analyze_resume
)

app = FastAPI(
    title="AI Resume Analyzer"
)


@app.get(
    "/health",
    response_model=HealthResponse
)
def health():

    return {
        "status": "healthy"
    }


@app.post(
    "/analyze",
    response_model=AnalysisResponse
)
async def analyze(
    resume: UploadFile = File(...),
    jd: str = Form(...)
):

    pdf_bytes = await resume.read()

    resume_text = extract_text_from_pdf(
        pdf_bytes
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

    return result