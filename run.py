# run.py

import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

if __name__ == "__main__":
    # Handle PORT variable - use default if not set (for local development)
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Starting Bajaj Policy System on {host}:{port}")
    
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=True
    )
