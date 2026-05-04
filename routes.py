from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.schemas import AnalysisResponse
from app.services.parser import extract_text_from_file
from app.services.analyzer import analyze_resume

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db)
):
    if not resume.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")
        
    # Read file content
    content = await resume.read()
    
    # Extract text
    try:
        resume_text = extract_text_from_file(content, resume.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse file: {str(e)}")
        
    # Run analysis
    result = analyze_resume(resume_text, job_description)
    
    return result
