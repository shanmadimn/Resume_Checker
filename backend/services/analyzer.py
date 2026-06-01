import re

from backend.services.skills import ALL_SKILLS
from backend.services.embeddings import semantic_similarity


def normalize(text: str) -> str:

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    return text


def extract_skills(text: str):

    text = normalize(text)

    found = []

    for skill in ALL_SKILLS:

        if skill in text:
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