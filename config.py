from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Resume Analyzer & Job Matcher"
    DATABASE_URL: str = "sqlite:///./resume_matcher.db"
    
    class Config:
        case_sensitive = True

settings = Settings()
