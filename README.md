# 📄 AI Resume Analyzer & Job Matcher

An AI-powered resume analysis platform that evaluates candidate-job fit using semantic similarity, ATS scoring, skill gap analysis, and LLM-generated recruiter feedback. The application goes beyond traditional keyword matching by leveraging NLP embeddings to understand contextual relevance between resumes and job descriptions.

## 🚀 Features

- 📑 Upload and analyze PDF resumes
- 🎯 ATS score calculation based on semantic similarity and skill matching
- 🧠 Context-aware resume-to-job matching using Sentence Transformers
- 🔍 Skill gap analysis with matched and missing skill identification
- 🤖 AI-generated recruiter feedback using Groq LLM
- ⚡ FastAPI backend with Pydantic validation
- 📊 Interactive Streamlit dashboard for analysis visualization
- 📖 Swagger API documentation for testing and development

## 🏗️ Architecture

Resume PDF → Text Extraction → Semantic Analysis → Skill Gap Detection → ATS Scoring → AI Feedback Generation → Dashboard Visualization

## 🛠️ Tech Stack

### Backend
- FastAPI
- Pydantic
- Uvicorn

### AI / NLP
- Sentence Transformers
- Scikit-learn
- Groq LLM

### Frontend
- Streamlit

### Document Processing
- PDFPlumber

### Programming Language
- Python

## 📂 Project Structure

```text
ai-resume-analyzer/
│
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   └── services/
│       ├── parser.py
│       ├── analyzer.py
│       ├── embeddings.py
│       └── llm_feedback.py
│
├── frontend/
│   └── streamlit_app.py
│
├── requirements.txt
├── .env
└── README.md
```

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/shanmadimn/resume-analyzer.git

cd resume-analyzer
```

### Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
MODEL_NAME=llama-3.3-70b-versatile
```

## ▶️ Run Backend

```bash
uvicorn backend.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## ▶️ Run Frontend

```bash
streamlit run frontend/streamlit_app.py
```

Application URL:

```text
http://localhost:8501
```

## 📊 Sample Output

### ATS Score

```text
ATS Score: 86%
Semantic Match: 83%
```

### Matched Skills

```text
Python
FastAPI
Machine Learning
PyTorch
LangChain
```

### Missing Skills

```text
AWS
Docker
Kubernetes
```

### AI Recruiter Feedback

```text
Strengths:
• Strong AI/ML experience
• Relevant backend development expertise

Weaknesses:
• Limited cloud exposure
• Missing deployment-related achievements

Recommendations:
• Highlight production deployments
• Showcase cloud-native projects
```

## 📸 Outputs

<img width="1898" height="873" alt="Screenshot 2026-06-02 023801" src="https://github.com/user-attachments/assets/844fa840-a4e0-41e9-bb63-eaf286d796cd" />
<img width="1909" height="876" alt="Screenshot 2026-06-02 023823" src="https://github.com/user-attachments/assets/b3a5bb46-cd4a-423a-894f-66d9425d8239" />
<img width="1903" height="886" alt="Screenshot 2026-06-02 023848" src="https://github.com/user-attachments/assets/33026391-6532-4c4d-b4c0-b19f110034b4" />

## 🎯 Key Learnings

- Semantic search using embeddings
- Resume-job matching using NLP
- REST API development with FastAPI
- LLM integration and prompt engineering
- ATS score computation
- Production-style backend architecture
- AI-powered recommendation systems

## 🔮 Future Enhancements

- Multi-resume ranking system
- Resume recommendation engine
- Interview question generation
- PDF report export
- Docker containerization
- AWS EC2 deployment
- Authentication and user profiles

## 👨‍💻 Author

**Sha**

AI Engineer | Machine Learning | NLP | LLM Applications

GitHub: https://github.com/shanmadimn

⭐ If you found this project useful, consider giving it a star.
