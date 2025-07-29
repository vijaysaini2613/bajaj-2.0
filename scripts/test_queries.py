# scripts/test_queries.py

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.pipeline import InferencePipeline
import tempfile

def test_sample_queries():
    """Test the system with sample queries"""
    
    # Load test queries
    with open("data/test_queries.json", "r") as f:
        test_queries = json.load(f)
    
    # Initialize pipeline
    pipeline = InferencePipeline()
    
    print("🧪 Running test queries...\n")
    
    for i, test in enumerate(test_queries, 1):
        print(f"{'='*60}")
        print(f"TEST {i}: {test['query']}")
        print(f"{'='*60}")
        
        # Create dummy PDF file for testing
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_file.write(b"Dummy PDF content for testing")
            temp_file.flush()
            
            try:
                # Run pipeline
                with open(temp_file.name, "rb") as pdf_file:
                    result = pipeline.run(
                        file_stream=pdf_file,
                        query=test["query"],
                        metadata=test["user_metadata"]
                    )
                
                # Display results
                print(f"📋 Query: {test['query']}")
                print(f"👤 User: Age {test['user_metadata']['age']}, Policy {test['user_metadata']['policy_duration']} days")
                print(f"🔍 Decision: {'✅ APPROVED' if result['claim_allowed'] else '❌ REJECTED'}")
                print(f"📄 Reason: {result['reason']}")
                print(f"📊 Confidence: {result['confidence_score']}")
                print(f"🎯 Expected: {'APPROVED' if test['expected_decision'] else 'REJECTED'}")
                
                # Check if result matches expectation
                if result['claim_allowed'] == test['expected_decision']:
                    print("✅ TEST PASSED")
                else:
                    print("❌ TEST FAILED - Decision mismatch")
                
                print()
                
            finally:
                os.unlink(temp_file.name)

if __name__ == "__main__":
    test_sample_queries()
