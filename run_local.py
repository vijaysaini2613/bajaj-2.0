#!/usr/bin/env python3
"""
Local development server for Bajaj Policy System
Handles environment variables and dependency issues
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if critical dependencies are installed"""
    try:
        import numpy
        print(f"NumPy version: {numpy.__version__}")
        
        # Check if NumPy version is compatible
        if numpy.__version__.startswith('2.'):
            print("⚠️  Warning: NumPy 2.x detected. This may cause FAISS compatibility issues.")
            print("   Consider downgrading: pip install 'numpy<2.0.0'")
            return False
            
        import faiss
        print(f"✅ FAISS imported successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main function to start the development server"""
    
    print("🚀 Starting Bajaj Policy System - Development Server")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 To fix dependencies:")
        print("1. pip install 'numpy<2.0.0'")
        print("2. pip install -r requirements.txt --force-reinstall")
        print("3. Or use: pip install -r requirements-minimal.txt")
        return
    
    # Set environment variables for local development
    os.environ["HOST"] = "0.0.0.0"
    os.environ["PORT"] = "8000"
    os.environ["ENVIRONMENT"] = "development"
    
    # Optional: Set API key for testing
    if not os.getenv("BAJAJ_API_KEY"):
        os.environ["BAJAJ_API_KEY"] = "test-key-local-development"
        print("🔑 Using test API key for local development")
    
    print(f"🌐 Starting server on http://localhost:8000")
    print(f"📖 API Documentation: http://localhost:8000/docs")
    print(f"🎯 Competition endpoint: http://localhost:8000/api/v1/hackrx/run")
    print("Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

if __name__ == "__main__":
    main()
