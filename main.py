from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import weaviate
import os
from dotenv import load_dotenv
from api import ingestion, rag
from services.weaviate_client import create_client
from services.schema import init_schema

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = create_client()
    init_schema(client)
    app.state.weaviate_client = client
    yield
    client.close()

def rag_app() -> FastAPI:
    app = FastAPI(
        title="Rag with Weaviate + HuggingFace models",
        version="1.0.0",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_headers=["*"],
        allow_methods=["*"],
    )

    app.include_router(ingestion.router, prefix="/ingestion", tags=["Ingestion"])
    app.include_router(rag.router, prefix="/rag", tags=["Rag"])

    return app

app = rag_app()
