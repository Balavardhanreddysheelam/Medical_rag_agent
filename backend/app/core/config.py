from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Medical RAG Agent"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # External APIs
    GROQ_API_KEY: str
    
    # Vector DB
    QDRANT_URL: str = "http://qdrant:6333"
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION_NAME: str = "medical_docs"
    
    # Model Config
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL: str = "llama-3.1-8b-instant"
    USE_FASTEMBED: bool = False # Disabled in favor of Cloud Embeddings
    USE_CLOUD_EMBEDDINGS: bool = True
    HUGGINGFACE_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
