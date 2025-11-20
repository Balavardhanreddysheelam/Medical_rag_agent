# Medical RAG Agent

A retrieval-augmented generation system for medical document analysis with automatic PHI redaction. This project demonstrates how to build a RAG pipeline that processes medical documents, redacts sensitive information, and provides intelligent query responses.

## Overview

This application allows users to upload medical PDFs, automatically redacts protected health information using named entity recognition, stores document chunks in a vector database, and answers questions using semantic search combined with large language models.

## Core Features

- PDF document upload and text extraction
- Automatic PHI redaction using spaCy NER
- Vector-based semantic search with Qdrant
- Query answering with Llama 3.1 via Groq API
- Streaming responses using server-sent events
- User authentication via Clerk
- Dockerized deployment

## Technical Stack

### Backend
- FastAPI for the REST API
- Qdrant for vector storage
- sentence-transformers for embeddings (all-MiniLM-L6-v2)
- Groq API for LLM inference (Llama 3.1 8B)
- spaCy for named entity recognition
- LangChain for RAG orchestration

### Frontend
- Next.js 15 with App Router
- shadcn/ui component library
- Tailwind CSS for styling
- Clerk for authentication

## Installation

### Prerequisites

- Docker and Docker Compose
- Node.js 18 or higher
- API keys for Groq and Clerk

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd medical-rag-agent
```

2. Create environment files:
```bash
cp .env.example .env
```

3. Add your API keys to `.env`:
```
GROQ_API_KEY=your_groq_api_key
CLERK_SECRET_KEY=your_clerk_secret_key
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
```

4. Update `frontend/.env.local` with Clerk keys:
```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key
```

5. Update the environment variables in `docker-compose.yml` to reference your keys.

### Running the Application

Start all services with Docker Compose:
```bash
docker-compose up --build
```

The backend will be available at http://localhost:8000 and the Qdrant dashboard at http://localhost:6333.

For local frontend development:
```bash
cd frontend
npm install
npm run dev
```

The frontend will run at http://localhost:3000.

## Usage

1. Sign in using Clerk authentication
2. Upload a medical PDF document
3. Wait for the processing confirmation
4. Ask questions about the document in the chat interface
5. Receive AI-generated answers based on the document content

## API Endpoints

- `GET /` - API root
- `GET /health` - Health check endpoint
- `POST /api/v1/upload` - Upload PDF file (rate limit: 5 requests/minute)
- `POST /api/v1/query` - Query the system (rate limit: 10 requests/minute)

## Project Structure

```
medical-rag-agent/
├── backend/
│   ├── app/
│   │   ├── api/routes.py           # API endpoints
│   │   ├── core/
│   │   │   ├── config.py           # Application configuration
│   │   │   └── vector_store.py     # Qdrant client setup
│   │   ├── models/api.py           # Request/response models
│   │   ├── services/
│   │   │   ├── ingestion.py        # PDF processing logic
│   │   │   ├── rag.py              # RAG query service
│   │   │   └── redaction.py        # PHI redaction service
│   │   └── main.py                 # FastAPI application
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── chat-interface.tsx
│   │   ├── upload-form.tsx
│   │   └── ui/                     # shadcn components
│   └── package.json
├── docker-compose.yml
└── .env.example
```

## PHI Redaction

The system uses spaCy's named entity recognition to identify and redact the following entity types:

- PERSON - Individual names
- DATE - Temporal information
- GPE - Geographic locations
- ORG - Organizations
- CARDINAL - Numeric values
- MONEY - Monetary amounts

Redacted entities are replaced with `[ENTITY_TYPE]` placeholders in the processed text.

## Development

### Backend Development

```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
cd backend
pytest
```

## Security Notes

This is a demonstration project and should not be used with real patient data in production without implementing proper HIPAA compliance measures. Production deployment would require:

- Encryption at rest and in transit
- Comprehensive audit logging
- Role-based access control
- HIPAA-compliant infrastructure
- Secure key management
- Regular security audits
- Data retention and disposal policies

## Troubleshooting

**Query returns "Could not retrieve answer"**
- Verify that at least one PDF has been uploaded
- Check that the Groq API key is valid
- Review backend logs for detailed error messages

**Upload fails**
- Ensure the file is a valid PDF
- Check backend logs for processing errors
- Verify Qdrant is running and accessible

**Frontend build errors**
- Clear the `.next` directory
- Delete `node_modules` and reinstall dependencies
- Check that all environment variables are set

## License

MIT License

## Acknowledgments

This project uses Groq for LLM inference, shadcn/ui for UI components, and Clerk for authentication.
