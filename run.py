# run.py

import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
