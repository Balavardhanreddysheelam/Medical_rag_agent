from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.models.api import UploadResponse, QueryRequest
from app.services.ingestion import ingestion_service
from app.services.rag import rag_service
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/upload", response_model=UploadResponse)
@limiter.limit("5/minute")
async def upload_file(request: Request, file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        chunks_count = await ingestion_service.process_pdf(file)
        return UploadResponse(
            filename=file.filename,
            message="File processed successfully",
            chunks_count=chunks_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
@limiter.limit("10/minute")
async def query_rag(request: Request, body: QueryRequest):
    try:
        return StreamingResponse(
            rag_service.query(body.query),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
