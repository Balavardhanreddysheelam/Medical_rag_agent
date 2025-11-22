import io
from typing import List
from fastapi import UploadFile
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings # Imported conditionally
from qdrant_client.http import models
from app.core.config import settings
from app.core.vector_store import qdrant_client
from app.services.redaction import redaction_service
import structlog
import uuid

logger = structlog.get_logger()

class IngestionService:
    def __init__(self):
        if not settings.HUGGINGFACE_API_KEY:
            raise ValueError("HUGGINGFACE_API_KEY is required for Cloud Embeddings. Please set it in environment variables.")
            
        from app.core.cloud_embeddings import LightCloudEmbeddings
        self.embeddings = LightCloudEmbeddings(
            api_key=settings.HUGGINGFACE_API_KEY,
            model=settings.EMBEDDING_MODEL
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        # self._ensure_collection() # Moved to startup event to avoid import-time connection errors

    def _ensure_collection(self):
        collections = qdrant_client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if settings.QDRANT_COLLECTION_NAME not in collection_names:
            qdrant_client.create_collection(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=768, # Dimension for all-mpnet-base-v2
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Created collection {settings.QDRANT_COLLECTION_NAME}")

    async def process_pdf(self, file: UploadFile) -> int:
        content = await file.read()
        pdf = PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        
        # Redact PHI
        redacted_text = redaction_service.redact(text)
        
        # Chunk text
        chunks = self.text_splitter.split_text(redacted_text)
        
        if not chunks:
            return 0

        # Embed and Upsert
        points = []
        embeddings = self.embeddings.embed_documents(chunks)
        
        for i, chunk in enumerate(chunks):
            points.append(models.PointStruct(
                id=str(uuid.uuid4()),
                vector=embeddings[i],
                payload={
                    "text": chunk,
                    "source": file.filename,
                    "chunk_index": i
                }
            ))
            
        qdrant_client.upsert(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            points=points
        )
        
        logger.info(f"Ingested {len(chunks)} chunks from {file.filename}")
        return len(chunks)

ingestion_service = IngestionService()
