import faiss
import numpy as np
import pickle
from typing import List, Tuple


class FAISSVectorStore:
    def __init__(self, dim: int, index_path: str = "vector_index.faiss", metadata_path: str = "metadata.pkl"):
        self.dim = dim
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add_embeddings(self, embedding_data: List[dict]):
        embeddings = np.array([item["embedding"] for item in embedding_data]).astype("float32")
        self.index.add(embeddings)
        self.metadata.extend([item["text"] for item in embedding_data])
        self._save_index()

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        query_embedding = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.metadata):
                results.append((self.metadata[idx], float(dist)))
        return results

    def _save_index(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def load_index(self):
        try:
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, "rb") as f:
                self.metadata = pickle.load(f)
        except FileNotFoundError:
            print(f"Index files not found. Starting with empty index.")
            # Initialize empty index and metadata
            self.index = faiss.IndexFlatL2(self.dim)
            self.metadata = []
        except Exception as e:
            print("Failed to load FAISS index or metadata:", e)
            self.index = faiss.IndexFlatL2(self.dim)
            self.metadata = []
