import os
import weaviate
from weaviate.auth import AuthApiKey
from weaviate.classes.init import Auth
from weaviate.classes.init import AdditionalConfig, Timeout
from dotenv import load_dotenv
from services.embeddings import embedder
load_dotenv()

weaviate_url = os.getenv("WEAVIATE_URL")
weaviate_api_key = os.getenv("WEAVIATE_API_KEY")

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
    skip_init_checks=True,
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)
    )
)

def create_client():
    """
    Create and return a Weaviate client (v4).
    """
    return weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=AuthApiKey(weaviate_api_key),
        skip_init_checks=True,  # optional, prevents gRPC health check errors
    )
def create_schema():
    schema = {
        "classes": [
            {
                "class": "DocumentChunk",
                "description": "A chunk of test from upload documents",
                "vectorizer": "none",
                "properties": [
                    {"name": "text", "dataType": ["text"]},
                    {"name": "metadata", "dataType": ["text"]},
                ]
            }
        ]
    }

    # client.schema.delete_all()
    # client.schema.create(schema)
    client.close()  # Free up resources
    
# def insert_chunk(chunk, vector, filename):
#     data_object = {
#         "text": chunk,
#         "metadata": filename,
#         "chunk_length": len(chunk)
#     }

#     response = client.data_object.create(
#         data_object=data_object,
#         class_name="DocumentChunk",
#         vector=vector
#     )

#     return response["id"]

def insert_chunk(chunk, vector, filename):
    collection = client.collections.get("DocumentChunk")

    props = {
        "text": chunk,
        "metadata": filename,
        "chunk_length": len(chunk)
    }

    result = collection.data.insert(
        properties=props,
        vector=vector
    )

    return result.uuid

def query_weaviate(query: str, limit: int = 3):
    """
    Query Weaviate for the most relevant document chunks.
    
    Args:
        query (str): The natural language query.
        limit (int): Number of results to return.

    Returns:
        List[dict]: A list of matched documents with text + metadata.
    """
    client = create_client()

    try:
        collection = client.collections.get("DocumentChunk")

        query_vector = embedder(query)

        response = collection.query.near_vector(
            near_vector=query_vector,
            limit=limit,
            return_properties=["text", "metadata"]
        )
        results = []
        
        for obj in response.objects:
            results.append({
                "id": obj.uuid,
                "text": obj.properties.get("text", ""),
                "metadata": obj.properties.get("metadata", ""),
            })
        return results

    finally:
        client.close()
