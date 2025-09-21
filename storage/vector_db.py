import os
import weaviate
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

class WeaviateClient:
    def __init__(self):
        if WEAVIATE_API_KEY:
            auth = weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY)
            self.client = weaviate.Client(url=WEAVIATE_URL, auth_client_secret=auth)
        else:
            self.client = weaviate.Client(url=WEAVIATE_URL)
        self._ensure_schema()

    def _ensure_schema(self):
        schema = {
            "classes": [
                {
                    "class": "DocumentChunk",
                    "description": "A chunk of a document",
                    "vectorizer": "none",
                    "properties": [
                        {"name": "text", "dataType": ["text"]},
                        {"name": "metadata", "dataType": ["text"]}
                    ]
                }
            ]
        }
        # safe create
        try:
            existing = self.client.schema.get()
            # if empty or missing class, create schema
            names = [c["class"] for c in existing.get("classes", [])] if existing else []
            if "DocumentChunk" not in names:
                self.client.schema.create(schema)
        except Exception:
            self.client.schema.delete_all()
            self.client.schema.create(schema)

    def upsert_object(self, obj_id: str, text: str, metadata: Dict[str, Any], vector: List[float]):
        data_object = {"text": text, "metadata": str(metadata)}
        self.client.data_object.create(data_object=data_object, class_name="DocumentChunk", uuid=obj_id, vector=vector)

    def query_near_vector(self, vector: List[float], top_k: int = 3) -> List[Dict]:
        resp = self.client.query.get("DocumentChunk", ["text", "metadata"]).with_near_vector({"vector": vector}).with_limit(top_k).do()
        hits = resp.get("data", {}).get("Get", {}).get("DocumentChunk", []) or []
        out = []
        for h in hits:
            out.append({"text": h.get("text", ""), "metadata": h.get("metadata")})
        return out
