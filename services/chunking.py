from typing import List
import re

def chunk_sliding(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    tokens = text.split()
    chunks = []
    i = 0
    while i < len(tokens):
        chunk = tokens[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size-overlap

    return chunks

def chunk_sentence(text:str, chunk_size: int = 500, max_sentence_len: int = 200)->List[str]:
    setences = re.split(r'(?<=[\.\?\!])\s+', text)
    chunks = []
    current = []
    current_len = 0
    
    for s in setences:
        s_len = len(s.split())

        if s_len > max_sentence_len:
            chunks.append(s)
            continue

        if current_len + s_len > chunk_size and current:
            chunks.append(" ".join(current))
            current = [s]
            current_len = s_len
        else:
            current.append(s)
            current_len += s_len
    
    if current:
        chunks.append(" ".join(current))

    return chunks

def chunk_paragraph(text: str) -> List[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return paragraphs
