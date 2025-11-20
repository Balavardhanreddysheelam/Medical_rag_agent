from pydantic import BaseModel
from typing import List, Optional

class HealthResponse(BaseModel):
    status: str

class UploadResponse(BaseModel):
    filename: str
    message: str
    chunks_count: int

class QueryRequest(BaseModel):
    query: str
    history: Optional[List[dict]] = None # For chat history

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
