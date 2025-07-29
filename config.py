# config.py

import os
from typing import Optional

# API Security Configuration
API_KEY = os.getenv("BAJAJ_API_KEY")  # For securing your API endpoints
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-here")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

# Third-party API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # If using OpenAI for enhanced responses
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # For Hugging Face models
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")  # If using Azure OpenAI
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

# PostgreSQL Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "bajaj_policy_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Embedding Model Configuration
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

# Embedding similarity threshold for clause matching
MATCH_THRESHOLD = float(os.getenv("MATCH_THRESHOLD", "0.75"))

# File Upload Configuration
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))  # 50MB max file size
ALLOWED_FILE_TYPES = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

# Other settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

# Validation function for required API keys
def validate_required_config():
    """Validate that all required configuration is present"""
    missing_vars = []
    
    if not API_KEY:
        missing_vars.append("BAJAJ_API_KEY")
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Optional: Initialize validation on import
# validate_required_config()
