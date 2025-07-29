# scripts/quick_setup.py

import os
import sys
import subprocess
import faiss
import pickle
import json

def create_minimal_faiss_index():
    """Create a minimal FAISS index so the system can start"""
    print("🔍 Creating minimal FAISS index...")
    
    # Create directory
    os.makedirs('models/faiss_index', exist_ok=True)
    
    # Create empty FAISS index
    index = faiss.IndexFlatL2(384)  # all-MiniLM-L6-v2 dimension
    faiss.write_index(index, 'models/faiss_index/index.faiss')
    
    # Create empty metadata
    with open('models/faiss_index/metadata.pkl', 'wb') as f:
        pickle.dump([], f)
    
    print("✅ Minimal FAISS index created")

def create_basic_sample_data():
    """Create basic sample data for testing"""
    print("📝 Creating basic sample data...")
    
    sample_clauses = [
        {
            "clause_text": "Claims for pre-existing medical conditions are excluded from coverage unless specifically declared and accepted by the insurer.",
            "section": "Exclusions",
            "code": "Code-Excl01",
            "clause_type": "exclusion",
            "policy_type": "health"
        },
        {
            "clause_text": "Coverage includes hospitalization expenses up to the sum insured amount.",
            "section": "Benefits",
            "code": "Code-Cover01",
            "clause_type": "coverage",
            "policy_type": "health"
        }
    ]
    
    # Save to file
    os.makedirs('data', exist_ok=True)
    with open('data/basic_clauses.json', 'w') as f:
        json.dump(sample_clauses, f, indent=2)
    
    print("✅ Basic sample data created")

def check_dependencies():
    """Check if required packages are installed"""
    print("📦 Checking dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'sentence-transformers', 
        'faiss-cpu', 'PyMuPDF', 'numpy', 'torch'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies available")
    return True

def test_basic_imports():
    """Test if core components can be imported"""
    print("🧪 Testing core imports...")
    
    try:
        sys.path.append(os.getcwd())
        from app.embedder import Embedder
        from app.vector_store import FAISSVectorStore
        from app.clause_matcher import ClauseMatcher
        print("✅ Core components import successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    print("🚀 Quick Setup for Bajaj Policy Query System")
    print("=" * 50)
    
    # Change to project directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    steps_passed = 0
    total_steps = 4
    
    # Step 1: Check dependencies
    if check_dependencies():
        steps_passed += 1
    else:
        print("\n❌ Setup failed at dependency check")
        print("Please run: pip install -r requirements.txt")
        return
    
    # Step 2: Create FAISS index
    try:
        create_minimal_faiss_index()
        steps_passed += 1
    except Exception as e:
        print(f"❌ Failed to create FAISS index: {e}")
        return
    
    # Step 3: Create sample data
    try:
        create_basic_sample_data()
        steps_passed += 1
    except Exception as e:
        print(f"❌ Failed to create sample data: {e}")
        return
    
    # Step 4: Test imports
    if test_basic_imports():
        steps_passed += 1
    else:
        print("❌ Import test failed")
        return
    
    print(f"\n🎉 Quick setup complete! ({steps_passed}/{total_steps} steps passed)")
    
    if steps_passed == total_steps:
        print("\n✅ System is ready for basic testing!")
        print("\nNext steps:")
        print("1. python run.py  # Start the API server")
        print("2. Visit http://localhost:8000  # Check health endpoint")
        print("3. python scripts/populate_database.py  # For full functionality")
        print("\n⚠️  Note: This is minimal setup. For full functionality, run populate_database.py")
    else:
        print(f"\n❌ Setup incomplete. {total_steps - steps_passed} issues remain.")

if __name__ == "__main__":
    main()
