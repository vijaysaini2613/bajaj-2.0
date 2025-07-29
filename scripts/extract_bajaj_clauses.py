# scripts/extract_bajaj_clauses.py

import sys
import os
import json
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.document_processor import DocumentProcessor
from app.embedder import Embedder
from app.vector_store import FAISSVectorStore
import psycopg2
from config import DATABASE_URL, EMBEDDING_MODEL_NAME

def extract_clauses_from_bajaj_pdf(pdf_path):
    """Extract policy clauses from Bajaj PDF document"""
    
    # Initialize document processor
    doc_processor = DocumentProcessor()
    
    # Extract text from PDF
    print(f"📄 Extracting text from: {pdf_path}")
    text = doc_processor.extract_text(pdf_path)
    
    # Split into sentences and filter for policy clauses
    sentences = text.split('.')
    clauses = []
    
    # Keywords that indicate policy clauses
    clause_keywords = [
        'exclusion', 'excluded', 'not covered', 'waiting period', 'coverage', 'covered',
        'benefit', 'claim', 'premium', 'policy', 'insured', 'treatment', 'medical',
        'hospitalization', 'condition', 'illness', 'accident', 'death', 'maternity',
        'dental', 'pre-existing', 'deductible', 'copay', 'sum insured'
    ]
    
    clause_counter = 1
    
    for sentence in sentences:
        sentence = sentence.strip()
        
        # Skip very short sentences
        if len(sentence) < 50:
            continue
            
        # Check if sentence contains policy-related keywords
        sentence_lower = sentence.lower()
        if any(keyword in sentence_lower for keyword in clause_keywords):
            
            # Determine clause type based on content
            clause_type = 'condition'  # default
            if any(word in sentence_lower for word in ['exclusion', 'excluded', 'not covered']):
                clause_type = 'exclusion'
            elif any(word in sentence_lower for word in ['coverage', 'covered', 'benefit']):
                clause_type = 'coverage'
            elif any(word in sentence_lower for word in ['waiting period', 'condition', 'require']):
                clause_type = 'condition'
                
            # Determine section
            section = 'General'
            if 'exclusion' in sentence_lower:
                section = 'Exclusions'
            elif any(word in sentence_lower for word in ['benefit', 'coverage']):
                section = 'Benefits'
            elif 'condition' in sentence_lower:
                section = 'Conditions'
                
            clause = {
                'clause_text': sentence,
                'section': section,
                'code': f'Bajaj-{clause_type.title()}-{clause_counter:02d}',
                'clause_type': clause_type,
                'policy_type': 'health'
            }
            
            clauses.append(clause)
            clause_counter += 1
    
    return clauses

def save_bajaj_clauses_to_json(clauses, output_file):
    """Save extracted clauses to JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(clauses, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved {len(clauses)} clauses to {output_file}")

def populate_database_with_bajaj_clauses(clauses):
    """Populate database with Bajaj clauses and embeddings"""
    
    # Initialize embedder
    embedder = Embedder(model_name=EMBEDDING_MODEL_NAME)
    
    # Generate embeddings
    clause_texts = [clause["clause_text"] for clause in clauses]
    print(f"🧠 Generating embeddings for {len(clause_texts)} clauses...")
    embeddings = embedder.get_embeddings(clause_texts)
    
    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    try:
        # Clear existing data
        cursor.execute("DELETE FROM policy_clauses WHERE code LIKE 'Bajaj-%'")
        
        # Insert new clauses
        for i, clause in enumerate(clauses):
            embedding_json = json.dumps(embeddings[i].tolist())
            
            cursor.execute("""
                INSERT INTO policy_clauses 
                (clause_text, section, code, clause_type, policy_type, embedding)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                clause["clause_text"],
                clause["section"],
                clause["code"],
                clause["clause_type"],
                clause["policy_type"],
                embedding_json
            ))
        
        conn.commit()
        print(f"✅ Successfully inserted {len(clauses)} Bajaj clauses with embeddings")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error inserting clauses: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def update_faiss_index_with_bajaj_clauses(clauses):
    """Update FAISS index with Bajaj clauses"""
    
    # Initialize components
    embedder = Embedder(model_name=EMBEDDING_MODEL_NAME)
    vector_store = FAISSVectorStore(
        dim=384,
        index_path="models/faiss_index/index.faiss",
        metadata_path="models/faiss_index/metadata.pkl"
    )
    
    # Generate embeddings
    embedding_data = embedder.embed_and_pack([clause["clause_text"] for clause in clauses])
    
    # Add to vector store
    vector_store.add_embeddings(embedding_data)
    
    print(f"✅ Successfully updated FAISS index with {len(clauses)} Bajaj clauses")

def main():
    # Path to your Bajaj PDF
    bajaj_pdf_path = r"c:\Users\saini\Downloads\BAJHLIP23020V012223.pdf"
    
    if not os.path.exists(bajaj_pdf_path):
        print(f"❌ PDF file not found: {bajaj_pdf_path}")
        return
    
    print("🚀 Processing Bajaj Insurance Policy Document...")
    
    # Extract clauses from PDF
    clauses = extract_clauses_from_bajaj_pdf(bajaj_pdf_path)
    
    if not clauses:
        print("❌ No clauses extracted from PDF")
        return
    
    print(f"📋 Extracted {len(clauses)} potential policy clauses")
    
    # Save to JSON for review
    save_bajaj_clauses_to_json(clauses, "data/bajaj_extracted_clauses.json")
    
    # Populate database
    print("💾 Populating database with Bajaj clauses...")
    populate_database_with_bajaj_clauses(clauses)
    
    # Update FAISS index
    print("🔍 Updating FAISS vector index...")
    update_faiss_index_with_bajaj_clauses(clauses)
    
    print("✅ Bajaj policy processing complete!")
    print("\nSample extracted clauses:")
    for i, clause in enumerate(clauses[:3]):
        print(f"\n{i+1}. Type: {clause['clause_type']}")
        print(f"   Section: {clause['section']}")
        print(f"   Code: {clause['code']}")
        print(f"   Text: {clause['clause_text'][:100]}...")

if __name__ == "__main__":
    main()
