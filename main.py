# # from dotenv import load_dotenv
# # load_dotenv()

# # import json
# # import os
# # import sys
# # from fastapi import FastAPI, Depends, HTTPException, status, Request
# # from fastapi.middleware.cors import CORSMiddleware
# # from sqlalchemy.orm import Session

# # # Add parent directory to path so database, models, etc. are importable
# # sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # from database import get_db
# # import models, schemas, auth
# # from logger import logger

# # app = FastAPI(
# #     title="Survey App API",
# #     version="1.0.0"
# # )

# # # FIXED: Properly format the fallback default string separated by a comma
# # ALLOWED_ORIGINS_RAW = os.getenv(
# #     "ALLOWED_ORIGINS",
# #     "http://localhost:5173,https://survey-app-pulse.vercel.app,http://localhost:3000"
# # )

# # ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS_RAW.split(",") if origin.strip()]

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=ALLOWED_ORIGINS,
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )


# # @app.get("/")
# # def root():
# #     return {"message": "Survey App API is running"}


# # @app.post("/auth/login", response_model=schemas.TokenResponse)
# # def login(
# #     payload: schemas.LoginRequest,
# #     request: Request,
# #     db: Session = Depends(get_db)
# # ):
# #     ip = request.client.host if request.client else "unknown"
# #     username = payload.username

# #     user = db.query(models.User).filter(
# #         models.User.username == username
# #     ).first()

# #     if not user or not auth.verify_password(
# #         payload.password,
# #         user.hashed_password
# #     ):
# #         # Structured JSON payload for Splunk to automatically flag failed logins
# #         log_payload = {
# #             "action": "login",
# #             "username": username,
# #             "ip": ip,
# #             "status": "failed",
# #             "reason": "Invalid credentials",
# #             "environment": os.getenv("ENVIRONMENT", "development")
# #         }
# #         logger.warning(json.dumps(log_payload))

# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="Invalid username or password",
# #             headers={"WWW-Authenticate": "Bearer"},
# #         )

# #     access_token = auth.create_access_token(
# #         data={
# #             "sub": user.username,
# #             "user_id": user.id
# #         }
# #     )

# #     # Structured JSON payload for Splunk to verify successful logging metrics
# #     log_payload = {
# #         "action": "login",
# #         "username": username,
# #         "ip": ip,
# #         "status": "success",
# #         "token_issued": True,
# #         "environment": os.getenv("ENVIRONMENT", "development")
# #     }
# #     logger.info(json.dumps(log_payload))

# #     return schemas.TokenResponse(
# #         access_token=access_token,
# #         token_type="bearer",
# #         user=schemas.UserOut(
# #             id=user.id,
# #             username=user.username,
# #             full_name=user.full_name,
# #         ),
# #     )


# # @app.get("/auth/me", response_model=schemas.UserOut)
# # def get_current_user(
# #     current_user: models.User = Depends(auth.get_current_user)
# # ):
# #     return schemas.UserOut(
# #         id=current_user.id,
# #         username=current_user.username,
# #         full_name=current_user.full_name,
# #     )


# # @app.get("/survey/stats")
# # def get_survey_stats(
# #     current_user: models.User = Depends(auth.get_current_user)
# # ):
# #     return {
# #         "total_surveys": 12,
# #         "active_surveys": 5,
# #         "responses_today": 48,
# #         "completion_rate": 73.4,
# #         "surveys": [
# #             {"id": 1, "title": "Customer Satisfaction Q2 2025", "responses": 234, "status": "active", "completion": 82},
# #             {"id": 2, "title": "Employee Engagement Survey", "responses": 87, "status": "active", "completion": 67},
# #             {"id": 3, "title": "Product Feedback - Mobile App", "responses": 156, "status": "active", "completion": 91},
# #             {"id": 4, "title": "NPS Survey - Enterprise Clients", "responses": 43, "status": "draft", "completion": 0},
# #             {"id": 5, "title": "Onboarding Experience 2025", "responses": 310, "status": "closed", "completion": 100},
# #         ],
# #     }

# from dotenv import load_dotenv
# load_dotenv()

# import json
# import os
# import sys
# from fastapi import FastAPI, Depends, HTTPException, status, Request
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session

# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from database import get_db
# import models, schemas, auth
# from logger import logger
# from splunk_logger import send_to_splunk

# app = FastAPI(
#     title="Survey App API",
#     version="1.0.0"
# )

# ALLOWED_ORIGINS_RAW = os.getenv(
#     "ALLOWED_ORIGINS",
#     "http://localhost:5173,https://survey-app-pulse.vercel.app,http://localhost:3000"
# )
# ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS_RAW.split(",") if origin.strip()]
# print(f"[CORS] Allowed origins: {ALLOWED_ORIGINS}", flush=True)

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
#         log_payload = {
#             "action": "login",
#             "username": username,
#             "ip": ip,
#             "status": "failed",
#             "reason": "Invalid credentials",
#             "environment": os.getenv("ENVIRONMENT", "production")
#         }
#         logger.warning(json.dumps(log_payload))

#         # Send failed login to Splunk HEC
#         send_to_splunk(
#             action="LOGIN_FAILED",
#             username=username,
#             ip=ip,
#             reason="Invalid credentials"
#         )

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

#     log_payload = {
#         "action": "login",
#         "username": username,
#         "ip": ip,
#         "status": "success",
#         "token_issued": True,
#         "environment": os.getenv("ENVIRONMENT", "production")
#     }
#     logger.info(json.dumps(log_payload))

#     # Send successful login to Splunk HEC
#     send_to_splunk(
#         action="LOGIN_SUCCESS",
#         username=username,
#         ip=ip
#     )

#     return schemas.TokenResponse(
#         access_token=access_token,
#         token_type="bearer",
#         user=schemas.UserOut(
#             id=current_user.id if False else user.id,
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

# Load .env.local first (development), fall back to .env (production)
load_dotenv('.env.local', override=True)
load_dotenv('.env', override=False)

import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db, engine, Base
import models, schemas, auth
from logger import logger
from splunk_logger import send_to_splunk

app = FastAPI(
    title="Survey App API",
    version="1.0.0"
)

# Create tables on startup — safe, skips existing tables
Base.metadata.create_all(bind=engine)

ALLOWED_ORIGINS_RAW = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,https://surveymatrix.tech,http://localhost:3000"
)
ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS_RAW.split(",") if origin.strip()]
print(f"[CORS] Allowed origins: {ALLOWED_ORIGINS}", flush=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

APP_URL = os.getenv("APP_URL", "https://surveymatrix.tech")


# ── Email helper ──────────────────────────────────────────────────────────────
def send_welcome_email(to_email: str, full_name: str, username: str, password: str):
    """
    Sends a welcome email to the newly registered user.
    Requires SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS in your .env
    """
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    if not all([smtp_host, smtp_user, smtp_pass]):
        logger.warning("SMTP credentials not configured — welcome email skipped.")
        return

    subject = "Welcome to SurveyMatrix 🎉"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0;padding:0;background:#f8fafc;font-family:'Segoe UI',Arial,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background:#f8fafc;padding:40px 0;">
        <tr>
          <td align="center">
            <table width="560" cellpadding="0" cellspacing="0"
                   style="background:#ffffff;border-radius:16px;overflow:hidden;
                          box-shadow:0 4px 24px rgba(0,0,0,0.08);">

              <!-- Header -->
              <tr>
                <td style="background:linear-gradient(135deg,#0d9488,#f59e0b);
                            padding:36px 40px;text-align:center;">
                  <span style="font-size:32px;font-weight:900;color:#fff;
                               font-family:'Segoe UI',Arial,sans-serif;
                               letter-spacing:-1px;">S</span>
                  <h1 style="margin:12px 0 0;color:#fff;font-size:22px;font-weight:700;
                              letter-spacing:-0.5px;">SurveyMatrix</h1>
                </td>
              </tr>

              <!-- Body -->
              <tr>
                <td style="padding:40px 40px 32px;">
                  <h2 style="margin:0 0 12px;font-size:20px;color:#0f172a;font-weight:700;">
                    Welcome to SurveyMatrix, {full_name or username}! 👋
                  </h2>
                  <p style="margin:0 0 24px;font-size:15px;color:#64748b;line-height:1.7;">
                    Your account has been created successfully. You're now part of the
                    SurveyMatrix community — the modern platform for surveys that actually
                    get answered.
                  </p>

                  <!-- Credentials box -->
                  <div style="background:#f0fdfa;border:1px solid #99f6e4;border-radius:12px;
                               padding:20px 24px;margin-bottom:28px;">
                    <p style="margin:0 0 10px;font-size:13px;font-weight:700;
                               color:#0d9488;text-transform:uppercase;letter-spacing:0.08em;">
                      Your Login Credentials
                    </p>
                    <table cellpadding="0" cellspacing="0" width="100%">
                      <tr>
                        <td style="font-size:14px;color:#475569;padding:4px 0;width:90px;">Username</td>
                        <td style="font-size:14px;color:#0f172a;font-weight:600;padding:4px 0;">{username}</td>
                      </tr>
                      <tr>
                        <td style="font-size:14px;color:#475569;padding:4px 0;">Password</td>
                        <td style="font-size:14px;color:#0f172a;font-weight:600;padding:4px 0;">{password}</td>
                      </tr>
                    </table>
                  </div>

                  <!-- CTA button -->
                  <div style="text-align:center;margin-bottom:28px;">
                    <a href="{APP_URL}/login"
                       style="display:inline-block;padding:14px 36px;
                              background:linear-gradient(135deg,#0d9488,#0f766e);
                              color:#fff;text-decoration:none;border-radius:10px;
                              font-size:15px;font-weight:700;
                              box-shadow:0 4px 16px rgba(13,148,136,0.35);">
                      Log in to SurveyMatrix →
                    </a>
                  </div>

                  <p style="margin:0;font-size:13px;color:#94a3b8;text-align:center;line-height:1.6;">
                    If you didn't create this account, please ignore this email.<br/>
                    Login URL: <a href="{APP_URL}/login" style="color:#0d9488;">{APP_URL}/login</a>
                  </p>
                </td>
              </tr>

              <!-- Footer -->
              <tr>
                <td style="background:#f8fafc;padding:20px 40px;text-align:center;
                            border-top:1px solid #e2e8f0;">
                  <p style="margin:0;font-size:12px;color:#94a3b8;">
                    © {2026} SurveyMatrix. All rights reserved.
                  </p>
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = smtp_user
    msg["To"]      = to_email
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, to_email, msg.as_string())
        logger.info(json.dumps({"action": "welcome_email", "to": to_email, "status": "sent"}))
    except Exception as e:
        logger.error(json.dumps({"action": "welcome_email", "to": to_email, "status": "failed", "error": str(e)}))


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Survey App API is running"}


# ── Register ──────────────────────────────────────────────────────────────────
@app.post("/auth/register", response_model=schemas.TokenResponse, status_code=201)
def register(
    payload: schemas.RegisterRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    ip = request.client.host if request.client else "unknown"

    # Check username uniqueness
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken. Please choose another.",
        )

    # Check email uniqueness
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    # Create user
    new_user = models.User(
        username=payload.username,
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=auth.hash_password(payload.password),
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Issue JWT immediately so user lands on dashboard
    access_token = auth.create_access_token(
        data={"sub": new_user.username, "user_id": new_user.id}
    )

    log_payload = {
        "action": "register",
        "username": payload.username,
        "email": payload.email,
        "ip": ip,
        "status": "success",
        "environment": os.getenv("ENVIRONMENT", "production"),
    }
    logger.info(json.dumps(log_payload))

    # Send welcome email (non-blocking — failure won't break registration)
    try:
        send_welcome_email(
            to_email=payload.email,
            full_name=payload.full_name or payload.username,
            username=payload.username,
            password=payload.password,   # plain text — shown once in welcome email
        )
    except Exception as e:
        logger.error(json.dumps({"action": "welcome_email_dispatch", "error": str(e)}))

    return schemas.TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=schemas.UserOut(
            id=new_user.id,
            username=new_user.username,
            full_name=new_user.full_name,
        ),
    )


# ── Login ─────────────────────────────────────────────────────────────────────
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

    if not user or not auth.verify_password(payload.password, user.hashed_password):
        log_payload = {
            "action": "login",
            "username": username,
            "ip": ip,
            "status": "failed",
            "reason": "Invalid credentials",
            "environment": os.getenv("ENVIRONMENT", "production"),
        }
        logger.warning(json.dumps(log_payload))
        send_to_splunk(action="LOGIN_FAILED", username=username, ip=ip, reason="Invalid credentials")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(
        data={"sub": user.username, "user_id": user.id}
    )

    log_payload = {
        "action": "login",
        "username": username,
        "ip": ip,
        "status": "success",
        "token_issued": True,
        "environment": os.getenv("ENVIRONMENT", "production"),
    }
    logger.info(json.dumps(log_payload))
    send_to_splunk(action="LOGIN_SUCCESS", username=username, ip=ip)

    return schemas.TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=schemas.UserOut(
            id=user.id,
            username=user.username,
            full_name=user.full_name,
        ),
    )


# ── Me ────────────────────────────────────────────────────────────────────────
@app.get("/auth/me", response_model=schemas.UserOut)
def get_me(
    current_user: models.User = Depends(auth.get_current_user)
):
    return schemas.UserOut(
        id=current_user.id,
        username=current_user.username,
        full_name=current_user.full_name,
    )


# ── Survey stats ──────────────────────────────────────────────────────────────
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
            {"id": 1, "title": "Customer Satisfaction Q2 2025",  "responses": 234, "status": "active", "completion": 82},
            {"id": 2, "title": "Employee Engagement Survey",      "responses": 87,  "status": "active", "completion": 67},
            {"id": 3, "title": "Product Feedback - Mobile App",   "responses": 156, "status": "active", "completion": 91},
            {"id": 4, "title": "NPS Survey - Enterprise Clients", "responses": 43,  "status": "draft",  "completion": 0 },
            {"id": 5, "title": "Onboarding Experience 2025",      "responses": 310, "status": "closed", "completion": 100},
        ],
    }