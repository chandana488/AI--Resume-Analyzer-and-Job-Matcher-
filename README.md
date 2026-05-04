# AI Resume Analyzer & Job Matcher

This is a production-quality, full-stack application that uses advanced NLP and Machine Learning techniques (Sentence Transformers & spaCy) to semantically match a candidate's resume with a job description. 

Unlike basic keyword matchers, this system understands the *context* of the text, providing a highly accurate match score, deep skill gap analysis, and personalized suggestions.

## Features

- Resume upload and processing
- AI-based resume analysis
- Job description matching
- Skill extraction and keyword analysis
- Resume scoring system
- REST API using FastAPI
- CORS-enabled backend for frontend integration
- Database integration for storing data
- Modular backend architecture

## Project Structure

```
ai-resume-matcher/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── api/
│   │   │   └── routes.py        # API endpoints
│   │   ├── core/
│   │   │   └── config.py        # Settings and configurations
│   │   ├── db/
│   │   │   ├── database.py      # SQLAlchemy setup
│   │   │   └── models.py        # DB schemas
│   │   └── services/
│   │       ├── analyzer.py      # Core NLP matching logic
│   │       ├── ml_models.py     # SentenceTransformers & spaCy loading
│   │       └── parser.py        # PDF & DOCX text extraction
│   ├── data/
│   │   ├── sample_jobs.csv      # Job mock database
│   │   └── skills_db.txt        # Dictionary of tech skills
│   └── requirements.txt         # Backend dependencies
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── src/                     # React App code (App.jsx, index.css, etc.)
└── README.md
```

---

## Installation Instructions

### 1. Backend Setup (FastAPI & ML)

1. Open a terminal and navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Download the `spaCy` model:
   ```bash
   python -m spacy download en_core_web_sm
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
   *The backend will now be running on `http://localhost:8000`*

### 2. Frontend Setup (React & Tailwind)

1. Open a new terminal and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install the Node modules:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The frontend will now be running on `http://localhost:5173`*

---

## How the AI Works

1. **Text Extraction**: The system uses `pdfplumber` to extract text from PDFs and `python-docx` for Word documents.
2. **Embedding Generation**: The extracted text and the inputted Job Description are passed into the `all-MiniLM-L6-v2` transformer model. This generates two dense 384-dimensional vectors representing the semantic meaning of the text.
3. **Cosine Similarity**: The system calculates the cosine similarity between the two vectors. A higher score means the resume's experience closely matches the requirements of the job.
4. **Skill Extraction**: The text is scanned against a database of technical skills (`skills_db.txt`). It compares the set of skills found in the resume against the job description to calculate gaps.

---
## Tech Stack

- FastAPI
- Python
- SQLAlchemy
- SQLite / PostgreSQL
- REST APIs
- CORS Middleware
- NLP / AI Processing 

## Running the Application

### Option 1: Start the Application

Run the FastAPI server using:

```bash
uvicorn main:app --reload

## Option 2: Manual Start
Step 1: Install Required Packages
pip install -r requirements.txt
Step 2: Start locally Server at:
 http://127.0.0.1:8000
