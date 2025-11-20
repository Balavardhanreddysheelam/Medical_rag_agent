from typing import AsyncGenerator
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from app.core.vector_store import qdrant_client
import structlog

logger = structlog.get_logger()

class RAGService:
    def __init__(self):
        logger.info(f"Initializing ChatGroq with model: {settings.LLM_MODEL}")
        self.llm = ChatGroq(
            temperature=0,
            model_name=settings.LLM_MODEL,
            groq_api_key=settings.GROQ_API_KEY
        )
        self.embeddings = None # Lazy load if needed, but we use qdrant for retrieval
        
        # We need the embedding model to embed the query
        if settings.USE_FASTEMBED:
            logger.info("Using FastEmbed for embeddings")
            from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
            # FastEmbed uses a different model name format or defaults. 
            # For compatibility with all-MiniLM-L6-v2, we can use the default or specify exact model.
            # "BAAI/bge-small-en-v1.5" is default and very good/fast. 
            # But to match "sentence-transformers/all-MiniLM-L6-v2", we can try to use that if supported, 
            # or just stick to a known good fast model. 
            # Let's use the default FastEmbed model which is lightweight and good.
            self.embedding_model = FastEmbedEmbeddings() 
        else:
            logger.info("Using SentenceTransformers for embeddings")
            from langchain_huggingface import HuggingFaceEmbeddings
            self.embedding_model = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

        self.prompt = ChatPromptTemplate.from_template(
            """You are a helpful medical assistant. Use the following pieces of redacted context to answer the question at the end.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            
            Context:
            {context}
            
            Question: {question}
            
            Answer:"""
        )

    async def query(self, question: str) -> AsyncGenerator[str, None]:
        # 1. Embed query
        query_vector = self.embedding_model.embed_query(question)
        
        # 2. Retrieve relevant chunks
        logger.info(f"Qdrant client type: {type(qdrant_client)}")
        logger.info(f"Qdrant client attributes: {dir(qdrant_client)}")
        
        try:
            search_result = qdrant_client.search(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                query_vector=query_vector,
                limit=3
            )
        except AttributeError:
            # Fallback to query_points if search is missing (unlikely but possible in some versions/configs)
            logger.warning("qdrant_client.search not found, trying query_points")
            search_result = qdrant_client.query_points(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                query=query_vector,
                limit=3
            ).points
        
        context = "\n\n".join([hit.payload["text"] for hit in search_result])
        
        # 3. Generate answer streaming
        chain = self.prompt | self.llm | StrOutputParser()
        
        async for chunk in chain.astream({"context": context, "question": question}):
            yield chunk

rag_service = RAGService()
