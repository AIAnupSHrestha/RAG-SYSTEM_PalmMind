from pydantic import BaseModel

class RAGQuery(BaseModel):
    session_id: str
    query: str