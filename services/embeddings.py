from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    'BAAI/bge-large-zh-v1.5',
    device="cpu"
    )

def embedder(chunks: list[str])-> list[list[float]]:
    return model.encode(chunks, normalize_embeddings=True)