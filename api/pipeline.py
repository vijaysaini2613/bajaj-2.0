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
        self.embedder = Embedder(model_name=EMBEDDING_MODEL_NAME)
        
        # Initialize vector store with embedding dimension (384 for all-MiniLM-L6-v2)
        self.vector_store = FAISSVectorStore(
            dim=384, 
            index_path="models/faiss_index/index.faiss",
            metadata_path="models/faiss_index/metadata.pkl"
        )
        
        self.clause_matcher = ClauseMatcher(
            embedder=self.embedder,
            store=self.vector_store,
            threshold=MATCH_THRESHOLD
        )
        
        self.decision_engine = DecisionEngine(clause_matcher=self.clause_matcher)
    
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