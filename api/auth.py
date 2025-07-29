# api/auth.py

from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta
from config import API_KEY, JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_HOURS

security = HTTPBearer()

def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verify API key for endpoint protection
    """
    if not credentials:
        raise HTTPException(status_code=401, detail="API key required")
    
    if credentials.credentials != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return credentials.credentials

def create_jwt_token(user_data: dict) -> str:
    """
    Create JWT token for user sessions
    """
    payload = {
        "user_data": user_data,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verify JWT token for protected routes
    """
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload["user_data"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Dependency for API key authentication
def require_api_key():
    return Depends(verify_api_key)

# Dependency for JWT authentication
def require_jwt_token():
    return Depends(verify_jwt_token)
