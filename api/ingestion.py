from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.extractor import extract_text
from services.chunking import chunk_sliding, chunk_sentence, chunk_paragraph
from services.embeddings import embedder
from services.weaviate_client import insert_chunk
from services.database import saveMetaData
from typing import Literal, Callable, List

router = APIRouter()

chunking_strategies: dict[str, Callable[[str], List[str]]] = {
    "sliding": chunk_sliding,
    "sentence": chunk_sentence,
    "paragraph": chunk_paragraph,
}

@router.post("/upload")
async def upload_document(
        file:UploadFile = File(...),
        chunk_strategy: Literal["sliding", "sentence", "paragraph"] = Form("sliding")
):
    try:
        file_byte = await file.read()
        text = extract_text(file_bytes=file_byte, filename=file.filename)
        if not text:
            raise HTTPException(status_code=400, detail="No text extracted from file")
        
        chunks = chunking_strategies.get(chunk_strategy)

        vectors = embedder(chunks=chunks)

        for chunk, vec in zip(chunks, vectors):
            chunk_length = len(chunk)
            weaviate_id = insert_chunk(chunk, vec, file.filename)
            saveMetaData(file.filename, chunk_strategy, weaviate_id, chunk_length=chunk_length)
        return {"status": "sucess", "chunk_stored": chunk_length}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
