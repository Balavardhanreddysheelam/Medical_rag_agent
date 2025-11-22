import httpx
from typing import List
from app.core.config import settings
import structlog

logger = structlog.get_logger()

class LightCloudEmbeddings:
    """
    A lightweight embedding client that uses Hugging Face Inference API.
    Implements the interface expected by LangChain (embed_documents, embed_query)
    but uses raw HTTP requests to save memory.
    """
    def __init__(self, api_key: str, model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model}"
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.timeout = 30.0 # seconds

    def _call_api(self, texts: List[str]) -> List[List[float]]:
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    self.api_url, 
                    headers=self.headers, 
                    json={"inputs": texts, "options": {"wait_for_model": True}}
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Cloud embedding failed: {e}")
            raise e

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # HF API has limits, so we might need to batch if texts is huge.
        # For this app, chunks are small enough.
        return self._call_api(texts)

    def embed_query(self, text: str) -> List[float]:
        result = self._call_api([text])
        return result[0]
