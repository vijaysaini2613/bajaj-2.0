# api/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .pipeline import InferencePipeline
from .auth import require_api_key, create_jwt_token
from app.response_builder import ResponseBuilder
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Bajaj Hack 6.0 – Intelligent Policy Query System",
    description="AI-powered insurance policy analysis and claim decision system",
    version="1.0.0"
)

# Allow all origins (configurable)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Inference Pipeline
pipeline = InferencePipeline()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Bajaj Hack 6.0 - Policy Query System is running!", "status": "healthy"}

@app.post("/auth/token")
async def get_access_token(user_id: str, api_key: str = Depends(require_api_key)):
    """Get JWT token for authenticated sessions"""
    try:
        token = create_jwt_token({"user_id": user_id, "timestamp": time.time()})
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token generation failed: {str(e)}")

@app.post("/query/")
async def query_insurance(
    file: UploadFile = File(...), 
    query: str = "",
    age: int = None,
    policy_duration: int = None,
    existing_conditions: bool = False,
    api_key: str = Depends(require_api_key)  # Require API key authentication
):
    try:
        start_time = time.time()
        
        # Validate input
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty.")
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")

        # Log the request
        logger.info(f"Processing query: {query[:100]}... for file: {file.filename}")

        # Prepare metadata
        metadata = {
            "age": age,
            "policy_duration": policy_duration,
            "existing_conditions": existing_conditions
        }

        # Run pipeline
        decision = pipeline.run(file.file, query, metadata)
        
        # Calculate processing time
        processing_time = round((time.time() - start_time) * 1000, 2)  # milliseconds
        decision["processing_time_ms"] = processing_time

        # Log the result
        logger.info(f"Query processed in {processing_time}ms. Decision: {decision.get('claim_allowed')}")

        # Return structured response
        return ResponseBuilder.build_success_response(decision)

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return ResponseBuilder.build_error_response(str(e))
