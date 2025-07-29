# scripts/populate_database.py

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.embedder import Embedder
from app.vector_store import FAISSVectorStore
import psycopg2
from config import DATABASE_URL, EMBEDDING_MODEL_NAME

def populate_policy_clauses():
    """Load sample policy clauses and generate embeddings"""
    
    # Load sample data
    with open("data/sample_policy_clauses.json", "r") as f:
        clauses = json.load(f)
    
    # Initialize embedder
    embedder = Embedder(model_name=EMBEDDING_MODEL_NAME)
    
    # Generate embeddings for all clauses
    clause_texts = [clause["clause_text"] for clause in clauses]
    embeddings = embedder.get_embeddings(clause_texts)
    
    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        # Insert clauses with embeddings
        for i, clause in enumerate(clauses):
            embedding_json = json.dumps(embeddings[i].tolist())
            
            cursor.execute("""
                INSERT INTO policy_clauses 
                (clause_text, section, code, clause_type, policy_type, embedding)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (code) DO UPDATE SET
                    clause_text = EXCLUDED.clause_text,
                    embedding = EXCLUDED.embedding,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                clause["clause_text"],
                clause["section"], 
                clause["code"],
                clause["clause_type"],
                clause["policy_type"],
                embedding_json
            ))
        
        conn.commit()
        print(f"✅ Successfully inserted {len(clauses)} policy clauses with embeddings")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error inserting clauses: {e}")
    finally:
        cursor.close()
        conn.close()

def populate_faiss_index():
    """Populate FAISS vector store with embeddings"""
    
    # Load sample data
    with open("data/sample_policy_clauses.json", "r") as f:
        clauses = json.load(f)
    
    # Initialize components
    embedder = Embedder(model_name=EMBEDDING_MODEL_NAME)
    vector_store = FAISSVectorStore(
        dim=384,  # all-MiniLM-L6-v2 dimension
        index_path="models/faiss_index/index.faiss",
        metadata_path="models/faiss_index/metadata.pkl"
    )
    
    # Generate embeddings
    embedding_data = embedder.embed_and_pack([clause["clause_text"] for clause in clauses])
    
    # Add to vector store
    vector_store.add_embeddings(embedding_data)
    
    print(f"✅ Successfully populated FAISS index with {len(clauses)} clauses")

if __name__ == "__main__":
    print("🚀 Populating database with sample data...")
    
    # First populate PostgreSQL
    populate_policy_clauses()
    
    # Then populate FAISS index
    populate_faiss_index()
    
    print("✅ Database population complete!")
