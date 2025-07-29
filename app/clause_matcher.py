from app.embedder import Embedder
from app.vector_store import FAISSVectorStore
from typing import Dict


class ClauseMatcher:
    def __init__(self, embedder: Embedder, store: FAISSVectorStore, threshold: float = 0.35):
        self.embedder = embedder
        self.store = store
        self.threshold = threshold
        self.store.load_index()

    def match_query(self, query: str) -> Dict:
        query_embedding = self.embedder.get_embeddings([query])[0]
        matches = self.store.search(query_embedding, top_k=3)

        if not matches:
            return {
                "match_found": False,
                "reason": "No similar clause found.",
                "confidence_score": 0.0
            }

        best_match, score = matches[0]

        # FAISS returns L2 distance, we invert for confidence
        confidence = max(1.0 - score, 0.0)

        if confidence < self.threshold:
            return {
                "match_found": False,
                "reason": "Confidence below threshold.",
                "reference_clause": best_match,
                "confidence_score": round(confidence, 3)
            }

        return {
            "match_found": True,
            "reference_clause": best_match,
            "confidence_score": round(confidence, 3)
        }
