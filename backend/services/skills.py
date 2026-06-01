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
