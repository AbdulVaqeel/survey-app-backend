import os
import json
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
import models
from logger import logger  # Imports your updated Splunk-aware logger

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b",
)

bearer_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta
        or timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> models.User:

    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        username: str = payload.get("sub")

        if username is None:
            # Log structural extraction anomalies straight to Splunk
            log_payload = {
                "action": "token_validation",
                "status": "failed",
                "reason": "Missing sub claim inside JWT payload",
                "environment": os.getenv("ENVIRONMENT", "development")
            }
            logger.warning(json.dumps(log_payload))
            raise credentials_exception

    except JWTError as e:
        # Capture signature issues, expired tokens, or malformed hashes
        log_payload = {
            "action": "token_validation",
            "status": "failed",
            "reason": f"JWT decoding exception: {str(e)}",
            "environment": os.getenv("ENVIRONMENT", "development")
        }
        logger.warning(json.dumps(log_payload))
        raise credentials_exception

    user = (
        db.query(models.User)
        .filter(models.User.username == username)
        .first()
    )

    if user is None:
        # Capture scenarios where token is valid but corresponding DB user profile was wiped
        log_payload = {
            "action": "token_validation",
            "username": username,
            "status": "failed",
            "reason": "Valid token provided but corresponding database user record not found",
            "environment": os.getenv("ENVIRONMENT", "development")
        }
        logger.warning(json.dumps(log_payload))
        raise credentials_exception

    # Optional background confirmation tracking (comment out if your routes get too noisy)
    log_payload = {
        "action": "user_session_verification",
        "username": username,
        "status": "success",
        "environment": os.getenv("ENVIRONMENT", "development")
    }
    logger.info(json.dumps(log_payload))

    return user