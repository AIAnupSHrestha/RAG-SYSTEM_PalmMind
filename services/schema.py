from weaviate.classes.config import Configure

def init_schema(client):
    """
    Ensure DocumentChunk collection exists.
    """
    existing = list(client.collections.list_all().keys())

    if "DocumentChunk" not in existing:
        client.collections.create(
            name="DocumentChunk",
            vectorizer_config=Configure.Vectorizer.none(),
            properties=[
                Configure.Property(name="text", data_type="text"),
                Configure.Property(name="metadata", data_type="text"),
            ]
        )
        print("Created collection: DocumentChunk")
    else:
        print("Collection DocumentChunk already exists")

    client.close()
