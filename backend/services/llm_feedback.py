from groq import Groq
from backend.config import settings

client = Groq(
    api_key=settings.GROQ_API_KEY
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
            model=settings.MODEL_NAME,
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