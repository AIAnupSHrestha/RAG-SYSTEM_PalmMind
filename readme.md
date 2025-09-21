# RAG System Backend for Palm Mind Technology Hiring Task

## Overview

This repository implements a backend system for a Retrieval-Augmented Generation (RAG) application, developed as part of the hiring process for Palm Mind Technology. The system provides two REST APIs built with FastAPI:

1. **Document Ingestion API**: Handles uploading of `.pdf` or `.txt` files, text extraction, chunking with selectable strategies, embedding generation, and storage in a vector database. Metadata is stored in a SQL database.
2. **Conversational RAG API**: Supports multi-turn conversational queries using a custom RAG pipeline (without RetrievalQAChain), with chat history managed via Redis Cloud. It also includes functionality to parse and handle interview booking requests (name, email, date, time), storing booking details in the database.

The codebase adheres to industry standards, including clean modular structure, type hints, and Pydantic models for request/response validation. No local vector stores like FAISS or Chroma are used, and there is no UI component. No LangChain libraries are used.

## Features

- **Document Ingestion**:
  - Supports uploading `.pdf` and `.txt` files via multipart form data.
  - Text extraction using PyPDF2 for PDFs and standard file reading for TXT.
  - Three selectable chunking strategies: 
    - Sliding window chunking.
    - Sentence-based chunking.
    - Paragraph-based chunking.
  - Embedding generation using BAAI/bge-large-zh-v1.5 model.
  - Embeddings stored in Weaviate (vector database).
  - Metadata (e.g., file name, chunk details, timestamps) stored in SQLite.

- **Conversational RAG**:
  - Custom RAG implementation: Retrieves relevant chunks from Weaviate based on query embeddings, augments the prompt, and generates responses using meta-llama/Llama-3.2-1B-Instruct LLM.
  - Redis Cloud used for session-based chat memory to maintain conversation history.
  - Handles multi-turn queries by incorporating chat history in the retrieval and generation process.
  - Interview booking support: Parses user input for name, email, date, and time; validates and stores in SQLite. Responds with confirmation.

- **Constraints Met**:
  - No use of FAISS, Chroma, or LangChain's RetrievalQAChain.
  - Modular code with separation of concerns (API routes, models, services).
  - Full type annotations and Pydantic for API schemas.
  - Environment variable configuration for database connections and model settings.

## Technologies Used

- **Framework**: FastAPI
- **Embedding**: BAAI/bge-large-zh-v1.5
- **LLM**: meta-llama/Llama-3.2-1B-Instruct
- **Vector Database**: Weaviate
- **Metadata Database**: SQLite (via SQLAlchemy)
- **Chat Memory**: Redis Cloud
- **Text Processing**: Custom implementations for chunking and embeddings
- **Other Libraries**: PyPDF2, python-dotenv, pydantic, uvicorn
- **Python Version**: 3.10+

## Project Structure

```
RAG-SYSTEM_PalmMind/
├── api/
│   ├── __init__.py
│   ├── ingestion.py     # Document ingestion API endpoint
│   └── rag.py           # Conversational RAG API endpoint
├── models/
│   ├── booking_model.py # Pydantic models for booking
│   └── rag_model.py     # Pydantic models for RAG requests/responses
├── services/
│   ├── __init__.py
│   ├── chunking.py      # Chunking strategy implementations
│   ├── database.py      # Database connection and queries (SQLite)
│   ├── embeddings.py    # Embedding generation logic
│   ├── extractor.py     # Text extraction from files
│   ├── llm.py           # LLM interaction for generation
│   ├── RedisMemory.py   # Redis-based chat memory
│   ├── schema.py        # Database schemas
│   └── weaviate_client.py # Weaviate client for vector storage
├── .gitignore
├── main.py              # FastAPI app entry point
├── README.md            # This file
└── requirements.txt     # Dependencies
```

## Installation

1. **Clone the Repository**:
   ```
   git clone https://github.com/AIAnupSHrestha/RAG-SYSTEM_PalmMind.git
   cd RAG-SYSTEM_PalmMind
   ```

2. **Set Up Virtual Environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Create a `.env` file and fill in the values:
     - `WEAVIATE_URL`: Weaviate instance URL.
     - `WEAVIATE_API_KEY`: Weaviate API key (if required).
     - `SQLITE_DB_PATH`: Path to SQLite database (e.g., `RAG_data.db`).
     - `REDIS_URL`: Redis Cloud connection string (e.g., `redis://default:password@redis-12345.c123.us-east-1-1.ec2.cloud.redislabs.com:12345/0`).
     - Other optional vars for chunk sizes, model paths, etc.

5. **Set Up Databases**:
   - Start Weaviate instance (locally or cloud-based).
   - Set up a Redis Cloud database (sign up at https://redis.io/ if needed; free tier available).
   - The SQLite database will be created automatically on first run.

6. **Run the Server**:
   ```
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`. Access docs at `/docs`.

## Usage

### API Endpoints

- **Document Ingestion**:
  - **Endpoint**: `POST /ingest`
  - **Request Body** (multipart):
    - `file`: The `.pdf` or `.txt` file.
    - `chunk_strategy`: String ("sliding", "sentence", or "paragraph").
  - **Response**: JSON with status and ingested document details.
  - **Example (cURL)**:
    ```
    curl -X POST "http://127.0.0.1:8000/ingest" -F "file=@/path/to/file.pdf" -F "chunk_strategy=sliding"
    ```

- **Conversational RAG**:
  - **Endpoint**: `POST /chat`
  - **Request Body** (JSON):
    - `query`: The user's message (string).
    - `session_id`: Unique session identifier for chat history (string).
  - **Response**: JSON with generated response and any booking confirmation.
  - **Example (cURL)**:
    ```
    curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d '{"query": "Tell me about RAG", "session_id": "user123"}'
    ```
  - **Booking Example**: If the query includes "Book interview for John Doe, john@example.com, 2025-10-01, 14:00", it will parse, store, and confirm.

## Notes

- **Custom RAG**: The RAG logic is implemented manually: Embed query → Retrieve top-k chunks from Weaviate → Build prompt with history and context → Generate with LLM.
- **Error Handling**: APIs include validation and error responses.
- **Testing**: Use FastAPI's built-in docs for interactive testing.
- **Commitment**: As per the task note, I confirm availability for at least 1 year with a 2-month notice period if selected.

For any questions, please contact me via the email thread.

Thank you for considering my submission!