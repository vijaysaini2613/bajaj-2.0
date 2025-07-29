# scripts/test_bajaj_queries.py

import sys
import os
import tempfile
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.pipeline import InferencePipeline

def test_with_bajaj_pdf():
    """Test queries using the actual Bajaj PDF"""
    
    bajaj_pdf_path = r"c:\Users\saini\Downloads\BAJHLIP23020V012223.pdf"
    
    if not os.path.exists(bajaj_pdf_path):
        print(f"❌ PDF file not found: {bajaj_pdf_path}")
        print("Please ensure the Bajaj PDF is at the correct location")
        return
    
    # Initialize pipeline
    try:
        pipeline = InferencePipeline()
    except Exception as e:
        print(f"❌ Failed to initialize pipeline: {e}")
        print("Make sure to run 'python scripts/populate_database.py' first")
        return
    
    # Test queries relevant to insurance policies
    test_queries = [
        {
            "query": "What is the waiting period for pre-existing diseases?",
            "metadata": {"age": 35, "policy_duration": 20, "existing_conditions": True}
        },
        {
            "query": "Are dental treatments covered?",
            "metadata": {"age": 28, "policy_duration": 100, "existing_conditions": False}
        },
        {
            "query": "Is maternity coverage included?",
            "metadata": {"age": 30, "policy_duration": 400, "existing_conditions": False}
        },
        {
            "query": "What about hospitalization expenses?",
            "metadata": {"age": 45, "policy_duration": 200, "existing_conditions": False}
        },
        {
            "query": "Are alternative treatments like Ayurveda covered?",
            "metadata": {"age": 40, "policy_duration": 150, "existing_conditions": False}
        },
        {
            "query": "Is plastic surgery covered?",
            "metadata": {"age": 32, "policy_duration": 80, "existing_conditions": False}
        }
    ]
    
    print("🧪 Testing Bajaj Insurance Policy with Real PDF...")
    print(f"📄 Using PDF: {os.path.basename(bajaj_pdf_path)}")
    print("=" * 80)
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n🔍 TEST {i}: {test['query']}")
        print("-" * 60)
        
        try:
            # Read the actual Bajaj PDF
            with open(bajaj_pdf_path, "rb") as pdf_file:
                result = pipeline.run(
                    file_stream=pdf_file,
                    query=test["query"],
                    metadata=test["metadata"]
                )
            
            # Display results
            print(f"👤 User Profile: Age {test['metadata']['age']}, "
                  f"Policy {test['metadata']['policy_duration']} days, "
                  f"Pre-existing: {test['metadata']['existing_conditions']}")
            
            print(f"🎯 Decision: {'✅ CLAIM APPROVED' if result['claim_allowed'] else '❌ CLAIM REJECTED'}")
            print(f"📝 Reason: {result['reason']}")
            
            if 'reference_clause' in result:
                clause_preview = result['reference_clause'][:150]
                print(f"📄 Reference: {clause_preview}{'...' if len(result['reference_clause']) > 150 else ''}")
            
            print(f"📊 Confidence: {result.get('confidence_score', 'N/A')}")
            
            if 'processing_time_ms' in result:
                print(f"⏱️  Processing Time: {result['processing_time_ms']}ms")
                
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            
        print()

def main():
    print("🚀 Bajaj Insurance Policy Testing with Real PDF")
    print("=" * 50)
    
    # Check if required files exist
    required_files = [
        "models/faiss_index/index.faiss",
        "models/faiss_index/metadata.pkl"
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print("⚠️  Missing required files:")
        for f in missing_files:
            print(f"   - {f}")
        print("\n📝 Please run these commands first:")
        print("   1. python scripts/populate_database.py")
        print("   2. python scripts/extract_bajaj_clauses.py")
        return
    
    test_with_bajaj_pdf()

if __name__ == "__main__":
    main()
