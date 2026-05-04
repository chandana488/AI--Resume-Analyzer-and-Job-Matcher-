# AI Resume Analyzer & Job Matcher

This is a production-quality, full-stack application that uses advanced NLP and Machine Learning techniques (Sentence Transformers & spaCy) to semantically match a candidate's resume with a job description. 

Unlike basic keyword matchers, this system understands the *context* of the text, providing a highly accurate match score, deep skill gap analysis, and personalized suggestions.

## Features

- **Semantic Matching**: Uses `sentence-transformers/all-MiniLM-L6-v2` to compute vector embeddings of both the resume and job description, comparing them with Cosine Similarity.
- **Skill Gap Analysis**: Extracts technical skills using custom Named Entity Recognition logic and compares them to find matches and gaps.
- **Explainable AI**: Provides concrete, actionable suggestions on how to improve the resume for the specific job description.
- **Job Recommendations**: Compares the user's resume against a database of jobs to recommend the best fitting roles.
- **Modern UI**: Built with React, Vite, and Tailwind CSS for a premium, responsive user experience.

---

## Folder Structure

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

## Local Setup Instructions

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

## Deployment Steps

### Backend Deployment (Render / Heroku)
1. Push your code to GitHub.
2. Create a new Web Service on Render.
3. Connect your repository.
4. Set the Build Command to: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
5. Set the Start Command to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment (Vercel)
1. Go to Vercel and create a new project.
2. Connect your GitHub repository.
3. Set the Root Directory to `frontend`.
4. Vercel will automatically detect Vite and configure the build settings (`npm run build`).
5. In Environment Variables, set `VITE_API_URL` to your deployed backend URL.
6. Click Deploy.
