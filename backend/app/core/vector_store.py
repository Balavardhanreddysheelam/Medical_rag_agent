from qdrant_client import QdrantClient
from app.core.config import settings

# Initialize Qdrant Client
# For local dev with docker, we use the URL from settings
# Initialize Qdrant Client
# For local dev with docker, we use the URL from settings
# For Cloud, we use URL + API Key
qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY
)

def get_qdrant_client():
    return qdrant_client
