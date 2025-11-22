import os
from langchain_groq import GroqEmbeddings
from app.core.config import settings
import sys

try:
    # Initialize Groq Embeddings
    # Note: We need to specify a model. Groq usually supports 'llama2-70b-4096' etc for chat, 
    # but for embeddings they might use different ones or not support it yet.
    # Let's try to list models or just try a standard one if documented.
    # Actually, langchain_groq documentation says it uses `nomic-embed-text-v1` or similar if available via Groq?
    # Let's try to initialize without model first or with a common one.
    
    # According to recent updates, Groq might not have a dedicated embedding endpoint publicly documented as 'free' 
    # in the same way. But let's try.
    
    # If GroqEmbeddings class exists, let's see if it works.
    embeddings = GroqEmbeddings(groq_api_key=settings.GROQ_API_KEY)
    
    text = "This is a test document."
    query_result = embeddings.embed_query(text)
    
    print(f"Success! Embedding length: {len(query_result)}")
    sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
