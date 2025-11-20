from qdrant_client import QdrantClient
from app.core.config import settings

# Initialize Qdrant Client
# For local dev with docker, we use the URL from settings
qdrant_client = QdrantClient(url=settings.QDRANT_URL)

def get_qdrant_client():
    return qdrant_client
