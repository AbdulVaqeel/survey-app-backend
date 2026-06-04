# from dotenv import load_dotenv
# load_dotenv()

# import json
# import os
# import sys
# from fastapi import FastAPI, Depends, HTTPException, status, Request
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session

# # Add parent directory to path so database, models, etc. are importable
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from database import get_db
# import models, schemas, auth
# from logger import logger

# app = FastAPI(
#     title="Survey App API",
#     version="1.0.0"
# )

# # FIXED: Properly format the fallback default string separated by a comma
# ALLOWED_ORIGINS_RAW = os.getenv(
#     "ALLOWED_ORIGINS",
#     "http://localhost:5173,https://survey-app-pulse.vercel.app,http://localhost:3000"
# )

# ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS_RAW.split(",") if origin.strip()]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# def root():
#     return {"message": "Survey App API is running"}


# @app.post("/auth/login", response_model=schemas.TokenResponse)
# def login(
#     payload: schemas.LoginRequest,
#     request: Request,
#     db: Session = Depends(get_db)
# ):
#     ip = request.client.host if request.client else "unknown"
#     username = payload.username

#     user = db.query(models.User).filter(
#         models.User.username == username
#     ).first()

#     if not user or not auth.verify_password(
#         payload.password,
#         user.hashed_password
#     ):
#         # Structured JSON payload for Splunk to automatically flag failed logins
#         log_payload = {
#             "action": "login",
#             "username": username,
#             "ip": ip,
#             "status": "failed",
#             "reason": "Invalid credentials",
#             "environment": os.getenv("ENVIRONMENT", "development")
#         }
#         logger.warning(json.dumps(log_payload))

#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     access_token = auth.create_access_token(
#         data={
#             "sub": user.username,
#             "user_id": user.id
#         }
#     )

#     # Structured JSON payload for Splunk to verify successful logging metrics
#     log_payload = {
#         "action": "login",
#         "username": username,
#         "ip": ip,
#         "status": "success",
#         "token_issued": True,
#         "environment": os.getenv("ENVIRONMENT", "development")
#     }
#     logger.info(json.dumps(log_payload))

#     return schemas.TokenResponse(
#         access_token=access_token,
#         token_type="bearer",
#         user=schemas.UserOut(
#             id=user.id,
#             username=user.username,
#             full_name=user.full_name,
#         ),
#     )


# @app.get("/auth/me", response_model=schemas.UserOut)
# def get_current_user(
#     current_user: models.User = Depends(auth.get_current_user)
# ):
#     return schemas.UserOut(
#         id=current_user.id,
#         username=current_user.username,
#         full_name=current_user.full_name,
#     )


# @app.get("/survey/stats")
# def get_survey_stats(
#     current_user: models.User = Depends(auth.get_current_user)
# ):
#     return {
#         "total_surveys": 12,
#         "active_surveys": 5,
#         "responses_today": 48,
#         "completion_rate": 73.4,
#         "surveys": [
#             {"id": 1, "title": "Customer Satisfaction Q2 2025", "responses": 234, "status": "active", "completion": 82},
#             {"id": 2, "title": "Employee Engagement Survey", "responses": 87, "status": "active", "completion": 67},
#             {"id": 3, "title": "Product Feedback - Mobile App", "responses": 156, "status": "active", "completion": 91},
#             {"id": 4, "title": "NPS Survey - Enterprise Clients", "responses": 43, "status": "draft", "completion": 0},
#             {"id": 5, "title": "Onboarding Experience 2025", "responses": 310, "status": "closed", "completion": 100},
#         ],
#     }

from dotenv import load_dotenv
load_dotenv()

import json
import os
import sys
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
import models, schemas, auth
from logger import logger
from splunk_logger import send_to_splunk

app = FastAPI(
    title="Survey App API",
    version="1.0.0"
)

ALLOWED_ORIGINS_RAW = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,https://survey-app-pulse.vercel.app,http://localhost:3000"
)
ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS_RAW.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Survey App API is running"}


@app.post("/auth/login", response_model=schemas.TokenResponse)
def login(
    payload: schemas.LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    ip = request.client.host if request.client else "unknown"
    username = payload.username

    user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if not user or not auth.verify_password(
        payload.password,
        user.hashed_password
    ):
        log_payload = {
            "action": "login",
            "username": username,
            "ip": ip,
            "status": "failed",
            "reason": "Invalid credentials",
            "environment": os.getenv("ENVIRONMENT", "production")
        }
        logger.warning(json.dumps(log_payload))

        # Send failed login to Splunk HEC
        send_to_splunk(
            action="LOGIN_FAILED",
            username=username,
            ip=ip,
            reason="Invalid credentials"
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id
        }
    )

    log_payload = {
        "action": "login",
        "username": username,
        "ip": ip,
        "status": "success",
        "token_issued": True,
        "environment": os.getenv("ENVIRONMENT", "production")
    }
    logger.info(json.dumps(log_payload))

    # Send successful login to Splunk HEC
    send_to_splunk(
        action="LOGIN_SUCCESS",
        username=username,
        ip=ip
    )

    return schemas.TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=schemas.UserOut(
            id=current_user.id if False else user.id,
            username=user.username,
            full_name=user.full_name,
        ),
    )


@app.get("/auth/me", response_model=schemas.UserOut)
def get_current_user(
    current_user: models.User = Depends(auth.get_current_user)
):
    return schemas.UserOut(
        id=current_user.id,
        username=current_user.username,
        full_name=current_user.full_name,
    )


@app.get("/survey/stats")
def get_survey_stats(
    current_user: models.User = Depends(auth.get_current_user)
):
    return {
        "total_surveys": 12,
        "active_surveys": 5,
        "responses_today": 48,
        "completion_rate": 73.4,
        "surveys": [
            {"id": 1, "title": "Customer Satisfaction Q2 2025", "responses": 234, "status": "active", "completion": 82},
            {"id": 2, "title": "Employee Engagement Survey", "responses": 87, "status": "active", "completion": 67},
            {"id": 3, "title": "Product Feedback - Mobile App", "responses": 156, "status": "active", "completion": 91},
            {"id": 4, "title": "NPS Survey - Enterprise Clients", "responses": 43, "status": "draft", "completion": 0},
            {"id": 5, "title": "Onboarding Experience 2025", "responses": 310, "status": "closed", "completion": 100},
        ],
    }