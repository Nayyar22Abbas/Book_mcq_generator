from typing import list

def chunk_text(text:str, chunk_size:int=2000, overlap: int = 150) -> list:

    words = text.split()
    chunks = []
    start  = 0

    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start += chunk_size - overlap

    return chunks