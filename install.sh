#!/bin/bash
echo "🐍 Forcing Python 3.10.9 installation..."

# Check current Python version
python --version

# Install compatible packages in order
echo "📦 Installing core dependencies..."
pip install --upgrade pip

echo "📦 Installing FastAPI stack..."
pip install fastapi==0.110.0 uvicorn==0.29.0 gunicorn==21.2.0

echo "📦 Installing auth dependencies..."
pip install PyJWT==2.8.0 python-multipart==0.0.6

echo "📦 Installing basic utilities..."
pip install python-dotenv==1.0.1 requests==2.31.0 orjson==3.9.0

echo "📦 Installing data processing..."
pip install numpy==1.24.3 pandas==2.1.4

echo "📦 Installing PyTorch..."
pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu

echo "📦 Installing AI/ML dependencies..."
pip install transformers==4.41.1 sentence-transformers==2.6.1

echo "📦 Installing FAISS..."
pip install faiss-cpu==1.7.4

echo "📦 Installing PDF processing..."
pip install PyMuPDF==1.24.4 docx2txt==0.8 beautifulsoup4==4.12.2

echo "✅ Installation complete!"
python --version
pip list | grep -E "(torch|pandas|numpy|faiss|sentence)"
