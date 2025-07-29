from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List


class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None  # Lazy loading

    @property
    def model(self):
        """Lazy load the model only when needed"""
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def get_embeddings(self, chunks: List[str]) -> List[np.ndarray]:
        return self.model.encode(chunks, show_progress_bar=False, convert_to_numpy=True)

    def embed_and_pack(self, chunks: List[str]) -> List[dict]:
        embeddings = self.get_embeddings(chunks)
        return [
            {"text": chunk, "embedding": embedding.tolist()}
            for chunk, embedding in zip(chunks, embeddings)
        ]
