# api/pipeline.py

import io
import tempfile
import os
from app.document_processor import DocumentProcessor
from app.embedder import Embedder
from app.vector_store import FAISSVectorStore
from app.clause_matcher import ClauseMatcher
from app.decision_engine import DecisionEngine
from config import EMBEDDING_MODEL_NAME, MATCH_THRESHOLD

class InferencePipeline:
    def __init__(self):
        self.document_processor = DocumentProcessor()
        # Lazy initialization - don't load heavy components at startup
        self._embedder = None
        self._vector_store = None
        self._clause_matcher = None
        self._decision_engine = None
        
    @property
    def embedder(self):
        """Lazy load embedder only when needed"""
        if self._embedder is None:
            self._embedder = Embedder(model_name=EMBEDDING_MODEL_NAME)
        return self._embedder
        
    @property
    def vector_store(self):
        """Lazy load vector store only when needed"""
        if self._vector_store is None:
            # Initialize vector store with embedding dimension 
            # paraphrase-albert-small-v2 = 768, all-MiniLM-L6-v2 = 384
            dim = 768 if "albert" in EMBEDDING_MODEL_NAME else 384
            self._vector_store = FAISSVectorStore(
                dim=dim, 
                index_path="models/faiss_index/index.faiss",
                metadata_path="models/faiss_index/metadata.pkl"
            )
        return self._vector_store
        
    @property 
    def clause_matcher(self):
        """Lazy load clause matcher only when needed"""
        if self._clause_matcher is None:
            self._clause_matcher = ClauseMatcher(
                embedder=self.embedder,
                store=self.vector_store,
                threshold=MATCH_THRESHOLD
            )
        return self._clause_matcher
        
    @property
    def decision_engine(self):
        """Lazy load decision engine only when needed"""
        if self._decision_engine is None:
            self._decision_engine = DecisionEngine()
        return self._decision_engine
    
    def run(self, file_stream, query: str, metadata: dict = None) -> dict:
        """
        Main pipeline execution
        Args:
            file_stream: PDF file stream from FastAPI UploadFile
            query: User's insurance query
            metadata: Optional metadata (age, conditions, etc.)
        """
        if metadata is None:
            metadata = {}
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            content = file_stream.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Extract text from PDF
            document_text = self.document_processor.extract_text(temp_file_path)
            
            # For now, we'll use the query directly for matching
            # In future, you could analyze the document content too
            
            # Evaluate the claim
            decision = self.decision_engine.evaluate_claim(query, metadata)
            
            return decision
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)