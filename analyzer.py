import os
import re
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from app.services.ml_models import get_embedding, nlp

# Load skills database
SKILLS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "skills_db.txt")
try:
    with open(SKILLS_FILE, 'r', encoding='utf-8') as f:
        KNOWN_SKILLS = set([line.strip().lower() for line in f.readlines() if line.strip()])
except FileNotFoundError:
    KNOWN_SKILLS = {"python", "react", "machine learning", "fastapi", "sql", "javascript"} # Fallback

def extract_skills(text: str) -> set:
    text_lower = text.lower()
    found_skills = set()
    for skill in KNOWN_SKILLS:
        # Check whole word match
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found_skills.add(skill)
    return found_skills

def get_job_recommendations(resume_embedding):
    jobs_file = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample_jobs.csv")
    recommendations = []
    try:
        df = pd.read_csv(jobs_file)
        if df.empty:
            return recommendations
            
        job_embeddings = [get_embedding(desc) for desc in df['description']]
        
        if job_embeddings:
            similarities = cosine_similarity([resume_embedding], job_embeddings)[0]
            df['score'] = similarities * 100
            
            top_jobs = df.sort_values(by='score', ascending=False).head(3)
            for _, row in top_jobs.iterrows():
                recommendations.append({
                    "job_title": row['title'],
                    "company": row['company'],
                    "match_score": round(row['score'], 2)
                })
    except Exception as e:
        print(f"Error loading jobs: {e}")
        
    return recommendations

def check_ats_compatibility(text: str) -> dict:
    ats_score = 100
    ats_feedback = []
    
    text_lower = text.lower()
    
    # Check for standard sections
    sections = ['experience', 'education', 'skills']
    missing_sections = [sec for sec in sections if sec not in text_lower]
    
    if missing_sections:
        ats_score -= len(missing_sections) * 10
        ats_feedback.append(f"Missing standard ATS sections: {', '.join(missing_sections).title()}.")
        
    # Check length
    word_count = len(text.split())
    if word_count < 200:
        ats_score -= 15
        ats_feedback.append("Resume is too short. ATS systems might rank it lower due to lack of detail.")
    elif word_count > 1000:
        ats_score -= 10
        ats_feedback.append("Resume is quite long. Consider keeping it concise (1-2 pages) for better readability.")
        
    if not ats_feedback:
        ats_feedback.append("Good section formatting and length detected.")
        
    return {"ats_score": max(0, ats_score), "ats_feedback": ats_feedback}

def analyze_resume_quality(text: str) -> dict:
    quality_feedback = []
    action_verbs_found = set()
    
    # Common strong action verbs
    strong_verbs = {
        'managed', 'developed', 'led', 'spearheaded', 'created', 'designed', 
        'implemented', 'improved', 'increased', 'reduced', 'resolved', 'optimized',
        'launched', 'achieved', 'delivered', 'built', 'directed', 'coordinated'
    }
    
    doc = nlp(text)
    # Extract verbs from spaCy POS tagging
    for token in doc:
        if token.pos_ == "VERB":
            verb_lemma = token.lemma_.lower()
            if verb_lemma in strong_verbs or token.text.lower() in strong_verbs:
                action_verbs_found.add(verb_lemma)
                
    action_verbs_list = list(action_verbs_found)
    
    if len(action_verbs_list) < 5:
        quality_feedback.append("Try using more strong action verbs (e.g., spearheaded, optimized) to describe your impact.")
    else:
        quality_feedback.append(f"Great use of action verbs! We found {len(action_verbs_list)} strong verbs.")
        
    return {
        "action_verbs": action_verbs_list,
        "quality_feedback": quality_feedback
    }

def analyze_resume(resume_text: str, job_description: str) -> dict:
    # 1. Semantic Matching
    res_emb = get_embedding(resume_text)
    job_emb = get_embedding(job_description)
    
    sim_score = cosine_similarity([res_emb], [job_emb])[0][0]
    match_score = max(0, min(100, round(sim_score * 100, 2))) # Clamp to 0-100
    
    # 2. Skill Extraction
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    
    matched_skills = list(resume_skills.intersection(job_skills))
    missing_skills = list(job_skills.difference(resume_skills))
    
    # 3. Suggestions
    suggestions = []
    if missing_skills:
        suggestions.append(f"Consider adding these missing skills: {', '.join(missing_skills[:5])}")
    
    if match_score < 50:
        suggestions.append("Your resume semantic match is low. Try tailoring your experience descriptions to closely match the phrasing in the job description.")
    elif match_score >= 80:
        suggestions.append("Great semantic match! Ensure your formatting is ATS-friendly.")
    
    if len(resume_skills) < 3:
        suggestions.append("We found very few technical skills in your resume. Make sure you have a dedicated 'Skills' section with relevant keywords.")
        
    # 4. Job Recommendations
    recommended_jobs = get_job_recommendations(res_emb)
    
    # 5. Advanced Analysis (ATS & Quality)
    ats_results = check_ats_compatibility(resume_text)
    quality_results = analyze_resume_quality(resume_text)
    
    return {
        "match_score": float(match_score),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "recommended_jobs": recommended_jobs,
        "ats_score": float(ats_results['ats_score']),
        "ats_feedback": ats_results['ats_feedback'],
        "action_verbs": quality_results['action_verbs'],
        "quality_feedback": quality_results['quality_feedback']
    }
