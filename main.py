# from fastapi import FastAPI, Depends, HTTPException, status, Request
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# import datetime

# from database import engine, get_db
# import models, schemas, auth
# from logger import logger

# models.Base.metadata.create_all(bind=engine)

# app = FastAPI(title="Survey App API", version="1.0.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",
#         "http://127.0.0.1:5173"
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# def root():
#     return {"message": "Survey App API is running"}


# @app.post("/auth/login", response_model=schemas.TokenResponse)
# def login(payload: schemas.LoginRequest, request: Request, db: Session = Depends(get_db)):
#     ip = request.client.host
#     username = payload.username

#     user = db.query(models.User).filter(
#         models.User.username == username
#     ).first()

#     if not user or not auth.verify_password(payload.password, user.hashed_password):
#         logger.warning(
#             f"action=LOGIN_FAILED | username={username} | ip={ip} | reason=Invalid credentials"
#         )
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     access_token = auth.create_access_token(data={"sub": user.username, "user_id": user.id})

#     logger.info(
#         f"action=LOGIN_SUCCESS | username={username} | ip={ip} | token_issued=true"
#     )

#     return schemas.TokenResponse(
#         access_token=access_token,
#         token_type="bearer",
#         user=schemas.UserOut(id=user.id, username=user.username, full_name=user.full_name),
#     )


# @app.get("/auth/me", response_model=schemas.UserOut)
# def get_current_user(current_user: models.User = Depends(auth.get_current_user)):
#     return schemas.UserOut(
#         id=current_user.id,
#         username=current_user.username,
#         full_name=current_user.full_name,
#     )


# @app.get("/survey/stats")
# def get_survey_stats(current_user: models.User = Depends(auth.get_current_user)):
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

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from database import get_db
import models, schemas, auth
from logger import logger

app = FastAPI(
    title="Survey App API",
    version="1.0.0"
)

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
).split(",")

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
        logger.warning(
            f"action=LOGIN_FAILED | username={username} | ip={ip} | reason=Invalid credentials"
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

    logger.info(
        f"action=LOGIN_SUCCESS | username={username} | ip={ip} | token_issued=true"
    )

    return schemas.TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=schemas.UserOut(
            id=user.id,
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
            {
                "id": 1,
                "title": "Customer Satisfaction Q2 2025",
                "responses": 234,
                "status": "active",
                "completion": 82,
            },
            {
                "id": 2,
                "title": "Employee Engagement Survey",
                "responses": 87,
                "status": "active",
                "completion": 67,
            },
            {
                "id": 3,
                "title": "Product Feedback - Mobile App",
                "responses": 156,
                "status": "active",
                "completion": 91,
            },
            {
                "id": 4,
                "title": "NPS Survey - Enterprise Clients",
                "responses": 43,
                "status": "draft",
                "completion": 0,
            },
            {
                "id": 5,
                "title": "Onboarding Experience 2025",
                "responses": 310,
                "status": "closed",
                "completion": 100,
            },
        ],
    }