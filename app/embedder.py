from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List


class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def get_embeddings(self, chunks: List[str]) -> List[np.ndarray]:
        return self.model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)

    def embed_and_pack(self, chunks: List[str]) -> List[dict]:
        embeddings = self.get_embeddings(chunks)
        return [
            {"text": chunk, "embedding": embedding.tolist()}
            for chunk, embedding in zip(chunks, embeddings)
        ]
