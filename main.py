# # # from dotenv import load_dotenv
# # # load_dotenv()

# # # import json
# # # import os
# # # import sys
# # # from fastapi import FastAPI, Depends, HTTPException, status, Request
# # # from fastapi.middleware.cors import CORSMiddleware
# # # from sqlalchemy.orm import Session

# # # # Add parent directory to path so database, models, etc. are importable
# # # sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # # from database import get_db
# # # import models, schemas, auth
# # # from logger import logger

# # # app = FastAPI(
# # #     title="Survey App API",
# # #     version="1.0.0"
# # # )

# # # # FIXED: Properly format the fallback default string separated by a comma
# # # ALLOWED_ORIGINS_RAW = os.getenv(
# # #     "ALLOWED_ORIGINS",
# # #     "http://localhost:5173,https://survey-app-pulse.vercel.app,http://localhost:3000"
# # # )

# # # ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS_RAW.split(",") if origin.strip()]

# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=ALLOWED_ORIGINS,
# # #     allow_credentials=True,
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )


# # # @app.get("/")
# # # def root():
# # #     return {"message": "Survey App API is running"}


# # # @app.post("/auth/login", response_model=schemas.TokenResponse)
# # # def login(
# # #     payload: schemas.LoginRequest,
# # #     request: Request,
# # #     db: Session = Depends(get_db)
# # # ):
# # #     ip = request.client.host if request.client else "unknown"
# # #     username = payload.username

# # #     user = db.query(models.User).filter(
# # #         models.User.username == username
# # #     ).first()

# # #     if not user or not auth.verify_password(
# # #         payload.password,
# # #         user.hashed_password
# # #     ):
# # #         # Structured JSON payload for Splunk to automatically flag failed logins
# # #         log_payload = {
# # #             "action": "login",
# # #             "username": username,
# # #             "ip": ip,
# # #             "status": "failed",
# # #             "reason": "Invalid credentials",
# # #             "environment": os.getenv("ENVIRONMENT", "development")
# # #         }
# # #         logger.warning(json.dumps(log_payload))

# # #         raise HTTPException(
# # #             status_code=status.HTTP_401_UNAUTHORIZED,
# # #             detail="Invalid username or password",
# # #             headers={"WWW-Authenticate": "Bearer"},
# # #         )

# # #     access_token = auth.create_access_token(
# # #         data={
# # #             "sub": user.username,
# # #             "user_id": user.id
# # #         }
# # #     )

# # #     # Structured JSON payload for Splunk to verify successful logging metrics
# # #     log_payload = {
# # #         "action": "login",
# # #         "username": username,
# # #         "ip": ip,
# # #         "status": "success",
# # #         "token_issued": True,
# # #         "environment": os.getenv("ENVIRONMENT", "development")
# # #     }
# # #     logger.info(json.dumps(log_payload))

# # #     return schemas.TokenResponse(
# # #         access_token=access_token,
# # #         token_type="bearer",
# # #         user=schemas.UserOut(
# # #             id=user.id,
# # #             username=user.username,
# # #             full_name=user.full_name,
# # #         ),
# # #     )


# # # @app.get("/auth/me", response_model=schemas.UserOut)
# # # def get_current_user(
# # #     current_user: models.User = Depends(auth.get_current_user)
# # # ):
# # #     return schemas.UserOut(
# # #         id=current_user.id,
# # #         username=current_user.username,
# # #         full_name=current_user.full_name,
# # #     )


# # # @app.get("/survey/stats")
# # # def get_survey_stats(
# # #     current_user: models.User = Depends(auth.get_current_user)
# # # ):
# # #     return {
# # #         "total_surveys": 12,
# # #         "active_surveys": 5,
# # #         "responses_today": 48,
# # #         "completion_rate": 73.4,
# # #         "surveys": [
# # #             {"id": 1, "title": "Customer Satisfaction Q2 2025", "responses": 234, "status": "active", "completion": 82},
# # #             {"id": 2, "title": "Employee Engagement Survey", "responses": 87, "status": "active", "completion": 67},
# # #             {"id": 3, "title": "Product Feedback - Mobile App", "responses": 156, "status": "active", "completion": 91},
# # #             {"id": 4, "title": "NPS Survey - Enterprise Clients", "responses": 43, "status": "draft", "completion": 0},
# # #             {"id": 5, "title": "Onboarding Experience 2025", "responses": 310, "status": "closed", "completion": 100},
# # #         ],
# # #     }

# # from dotenv import load_dotenv
# # load_dotenv()

# # import json
# # import os
# # import sys
# # from fastapi import FastAPI, Depends, HTTPException, status, Request
# # from fastapi.middleware.cors import CORSMiddleware
# # from sqlalchemy.orm import Session

# # sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # from database import get_db
# # import models, schemas, auth
# # from logger import logger
# # from splunk_logger import send_to_splunk

# # app = FastAPI(
# #     title="Survey App API",
# #     version="1.0.0"
# # )

# # ALLOWED_ORIGINS_RAW = os.getenv(
# #     "ALLOWED_ORIGINS",
# #     "http://localhost:5173,https://survey-app-pulse.vercel.app,http://localhost:3000"
# # )
# # ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS_RAW.split(",") if origin.strip()]
# # print(f"[CORS] Allowed origins: {ALLOWED_ORIGINS}", flush=True)

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
# #         log_payload = {
# #             "action": "login",
# #             "username": username,
# #             "ip": ip,
# #             "status": "failed",
# #             "reason": "Invalid credentials",
# #             "environment": os.getenv("ENVIRONMENT", "production")
# #         }
# #         logger.warning(json.dumps(log_payload))

# #         # Send failed login to Splunk HEC
# #         send_to_splunk(
# #             action="LOGIN_FAILED",
# #             username=username,
# #             ip=ip,
# #             reason="Invalid credentials"
# #         )

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

# #     log_payload = {
# #         "action": "login",
# #         "username": username,
# #         "ip": ip,
# #         "status": "success",
# #         "token_issued": True,
# #         "environment": os.getenv("ENVIRONMENT", "production")
# #     }
# #     logger.info(json.dumps(log_payload))

# #     # Send successful login to Splunk HEC
# #     send_to_splunk(
# #         action="LOGIN_SUCCESS",
# #         username=username,
# #         ip=ip
# #     )

# #     return schemas.TokenResponse(
# #         access_token=access_token,
# #         token_type="bearer",
# #         user=schemas.UserOut(
# #             id=current_user.id if False else user.id,
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

# # Load .env.local first (development), fall back to .env (production)
# load_dotenv('.env.local', override=True)
# load_dotenv('.env', override=False)

# import sys
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# from fastapi import FastAPI, Depends, HTTPException, status, Request
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session

# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from database import get_db, engine, Base
# import models, schemas, auth
# from logger import logger
# from splunk_logger import send_to_splunk

# app = FastAPI(
#     title="Survey App API",
#     version="1.0.0"
# )

# # Create tables on startup — safe, skips existing tables
# Base.metadata.create_all(bind=engine)

# ALLOWED_ORIGINS_RAW = os.getenv(
#     "ALLOWED_ORIGINS",
#     "http://localhost:5173,https://surveymatrix.tech,http://localhost:3000"
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

# APP_URL = os.getenv("APP_URL", "https://surveymatrix.tech")


# # ── Email helper ──────────────────────────────────────────────────────────────
# def send_welcome_email(to_email: str, full_name: str, username: str, password: str):
#     """
#     Sends a welcome email to the newly registered user.
#     Requires SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS in your .env
#     """
#     smtp_host = os.getenv("SMTP_HOST")
#     smtp_port = int(os.getenv("SMTP_PORT", "587"))
#     smtp_user = os.getenv("SMTP_USER")
#     smtp_pass = os.getenv("SMTP_PASS")

#     if not all([smtp_host, smtp_user, smtp_pass]):
#         logger.warning("SMTP credentials not configured — welcome email skipped.")
#         return

#     subject = "Welcome to SurveyMatrix 🎉"

#     html_body = f"""
#     <!DOCTYPE html>
#     <html>
#     <body style="margin:0;padding:0;background:#f8fafc;font-family:'Segoe UI',Arial,sans-serif;">
#       <table width="100%" cellpadding="0" cellspacing="0" style="background:#f8fafc;padding:40px 0;">
#         <tr>
#           <td align="center">
#             <table width="560" cellpadding="0" cellspacing="0"
#                    style="background:#ffffff;border-radius:16px;overflow:hidden;
#                           box-shadow:0 4px 24px rgba(0,0,0,0.08);">

#               <!-- Header -->
#               <tr>
#                 <td style="background:linear-gradient(135deg,#0d9488,#f59e0b);
#                             padding:36px 40px;text-align:center;">
#                   <span style="font-size:32px;font-weight:900;color:#fff;
#                                font-family:'Segoe UI',Arial,sans-serif;
#                                letter-spacing:-1px;">S</span>
#                   <h1 style="margin:12px 0 0;color:#fff;font-size:22px;font-weight:700;
#                               letter-spacing:-0.5px;">SurveyMatrix</h1>
#                 </td>
#               </tr>

#               <!-- Body -->
#               <tr>
#                 <td style="padding:40px 40px 32px;">
#                   <h2 style="margin:0 0 12px;font-size:20px;color:#0f172a;font-weight:700;">
#                     Welcome to SurveyMatrix, {full_name or username}! 👋
#                   </h2>
#                   <p style="margin:0 0 24px;font-size:15px;color:#64748b;line-height:1.7;">
#                     Your account has been created successfully. You're now part of the
#                     SurveyMatrix community — the modern platform for surveys that actually
#                     get answered.
#                   </p>

#                   <!-- Credentials box -->
#                   <div style="background:#f0fdfa;border:1px solid #99f6e4;border-radius:12px;
#                                padding:20px 24px;margin-bottom:28px;">
#                     <p style="margin:0 0 10px;font-size:13px;font-weight:700;
#                                color:#0d9488;text-transform:uppercase;letter-spacing:0.08em;">
#                       Your Login Credentials
#                     </p>
#                     <table cellpadding="0" cellspacing="0" width="100%">
#                       <tr>
#                         <td style="font-size:14px;color:#475569;padding:4px 0;width:90px;">Username</td>
#                         <td style="font-size:14px;color:#0f172a;font-weight:600;padding:4px 0;">{username}</td>
#                       </tr>
#                       <tr>
#                         <td style="font-size:14px;color:#475569;padding:4px 0;">Password</td>
#                         <td style="font-size:14px;color:#0f172a;font-weight:600;padding:4px 0;">{password}</td>
#                       </tr>
#                     </table>
#                   </div>

#                   <!-- CTA button -->
#                   <div style="text-align:center;margin-bottom:28px;">
#                     <a href="{APP_URL}/login"
#                        style="display:inline-block;padding:14px 36px;
#                               background:linear-gradient(135deg,#0d9488,#0f766e);
#                               color:#fff;text-decoration:none;border-radius:10px;
#                               font-size:15px;font-weight:700;
#                               box-shadow:0 4px 16px rgba(13,148,136,0.35);">
#                       Log in to SurveyMatrix →
#                     </a>
#                   </div>

#                   <p style="margin:0;font-size:13px;color:#94a3b8;text-align:center;line-height:1.6;">
#                     If you didn't create this account, please ignore this email.<br/>
#                     Login URL: <a href="{APP_URL}/login" style="color:#0d9488;">{APP_URL}/login</a>
#                   </p>
#                 </td>
#               </tr>

#               <!-- Footer -->
#               <tr>
#                 <td style="background:#f8fafc;padding:20px 40px;text-align:center;
#                             border-top:1px solid #e2e8f0;">
#                   <p style="margin:0;font-size:12px;color:#94a3b8;">
#                     © {2026} SurveyMatrix. All rights reserved.
#                   </p>
#                 </td>
#               </tr>

#             </table>
#           </td>
#         </tr>
#       </table>
#     </body>
#     </html>
#     """

#     msg = MIMEMultipart("alternative")
#     msg["Subject"] = subject
#     msg["From"]    = smtp_user
#     msg["To"]      = to_email
#     msg.attach(MIMEText(html_body, "html"))

#     try:
#         with smtplib.SMTP(smtp_host, smtp_port) as server:
#             server.ehlo()
#             server.starttls()
#             server.login(smtp_user, smtp_pass)
#             server.sendmail(smtp_user, to_email, msg.as_string())
#         logger.info(json.dumps({"action": "welcome_email", "to": to_email, "status": "sent"}))
#     except Exception as e:
#         logger.error(json.dumps({"action": "welcome_email", "to": to_email, "status": "failed", "error": str(e)}))


# # ── Routes ────────────────────────────────────────────────────────────────────

# @app.get("/")
# def root():
#     return {"message": "Survey App API is running"}


# # ── Register ──────────────────────────────────────────────────────────────────
# @app.post("/auth/register", response_model=schemas.TokenResponse, status_code=201)
# def register(
#     payload: schemas.RegisterRequest,
#     request: Request,
#     db: Session = Depends(get_db)
# ):
#     ip = request.client.host if request.client else "unknown"

#     # Check username uniqueness
#     if db.query(models.User).filter(models.User.username == payload.username).first():
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="Username already taken. Please choose another.",
#         )

#     # Check email uniqueness
#     if db.query(models.User).filter(models.User.email == payload.email).first():
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="An account with this email already exists.",
#         )

#     # Create user
#     new_user = models.User(
#         username=payload.username,
#         email=payload.email,
#         full_name=payload.full_name,
#         hashed_password=auth.hash_password(payload.password),
#         is_active=True,
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     # Issue JWT immediately so user lands on dashboard
#     access_token = auth.create_access_token(
#         data={"sub": new_user.username, "user_id": new_user.id}
#     )

#     log_payload = {
#         "action": "register",
#         "username": payload.username,
#         "email": payload.email,
#         "ip": ip,
#         "status": "success",
#         "environment": os.getenv("ENVIRONMENT", "production"),
#     }
#     logger.info(json.dumps(log_payload))

#     # Send welcome email (non-blocking — failure won't break registration)
#     try:
#         send_welcome_email(
#             to_email=payload.email,
#             full_name=payload.full_name or payload.username,
#             username=payload.username,
#             password=payload.password,   # plain text — shown once in welcome email
#         )
#     except Exception as e:
#         logger.error(json.dumps({"action": "welcome_email_dispatch", "error": str(e)}))

#     return schemas.TokenResponse(
#         access_token=access_token,
#         token_type="bearer",
#         user=schemas.UserOut(
#             id=new_user.id,
#             username=new_user.username,
#             full_name=new_user.full_name,
#         ),
#     )


# # ── Login ─────────────────────────────────────────────────────────────────────
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

#     if not user or not auth.verify_password(payload.password, user.hashed_password):
#         log_payload = {
#             "action": "login",
#             "username": username,
#             "ip": ip,
#             "status": "failed",
#             "reason": "Invalid credentials",
#             "environment": os.getenv("ENVIRONMENT", "production"),
#         }
#         logger.warning(json.dumps(log_payload))
#         send_to_splunk(action="LOGIN_FAILED", username=username, ip=ip, reason="Invalid credentials")

#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     access_token = auth.create_access_token(
#         data={"sub": user.username, "user_id": user.id}
#     )

#     log_payload = {
#         "action": "login",
#         "username": username,
#         "ip": ip,
#         "status": "success",
#         "token_issued": True,
#         "environment": os.getenv("ENVIRONMENT", "production"),
#     }
#     logger.info(json.dumps(log_payload))
#     send_to_splunk(action="LOGIN_SUCCESS", username=username, ip=ip)

#     return schemas.TokenResponse(
#         access_token=access_token,
#         token_type="bearer",
#         user=schemas.UserOut(
#             id=user.id,
#             username=user.username,
#             full_name=user.full_name,
#         ),
#     )


# # ── Me ────────────────────────────────────────────────────────────────────────
# @app.get("/auth/me", response_model=schemas.UserOut)
# def get_me(
#     current_user: models.User = Depends(auth.get_current_user)
# ):
#     return schemas.UserOut(
#         id=current_user.id,
#         username=current_user.username,
#         full_name=current_user.full_name,
#     )


# # ── Survey stats ──────────────────────────────────────────────────────────────
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
#             {"id": 1, "title": "Customer Satisfaction Q2 2025",  "responses": 234, "status": "active", "completion": 82},
#             {"id": 2, "title": "Employee Engagement Survey",      "responses": 87,  "status": "active", "completion": 67},
#             {"id": 3, "title": "Product Feedback - Mobile App",   "responses": 156, "status": "active", "completion": 91},
#             {"id": 4, "title": "NPS Survey - Enterprise Clients", "responses": 43,  "status": "draft",  "completion": 0 },
#             {"id": 5, "title": "Onboarding Experience 2025",      "responses": 310, "status": "closed", "completion": 100},
#         ],
#     }


from dotenv import load_dotenv
load_dotenv('.env.local', override=True)
load_dotenv('.env', override=False)

import json, os, sys, io, csv, secrets, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from collections import Counter
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db, engine, Base
import models, schemas, auth
from logger import logger
from export_utils import generate_qr_code, export_to_excel, export_to_pptx, export_to_pdf

app = FastAPI(title="SurveyMatrix API", version="2.0.0")

# Auto-create all NEW tables on startup (never touches existing tables/columns/data)
Base.metadata.create_all(bind=engine)


def run_startup_migrations():
    """
    Best-effort, additive-only schema patch for columns added to EXISTING tables
    after they were first created (create_all only creates brand-new tables, it
    never alters ones that already exist). Every statement is wrapped so a failure
    here (wrong DB engine, missing permissions, etc.) can never take the API down
    or affect auth/login, which only ever touches the untouched `users` table.
    """
    statements = [
        "ALTER TABLE surveys ADD COLUMN IF NOT EXISTS requires_invite BOOLEAN DEFAULT FALSE",
        "ALTER TABLE responses ADD COLUMN IF NOT EXISTS invite_id INTEGER REFERENCES invites(id) ON DELETE SET NULL",
    ]
    try:
        with engine.connect() as conn:
            for stmt in statements:
                try:
                    conn.execute(text(stmt))
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    logger.warning(f"[migration] skipped ({e})")
    except Exception as e:
        logger.error(f"[migration] could not open connection: {e}")


run_startup_migrations()

ALLOWED_ORIGINS_RAW = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,https://surveymatrix.tech,http://localhost:3000"
)
ALLOWED_ORIGINS = [o.strip() for o in ALLOWED_ORIGINS_RAW.split(",") if o.strip()]
print(f"[CORS] Allowed origins: {ALLOWED_ORIGINS}", flush=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

APP_URL = os.getenv("APP_URL", "https://surveymatrix.tech")


# ── Welcome email ─────────────────────────────────────────────────────────────
def send_welcome_email(to_email, full_name, username, password):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    if not all([smtp_host, smtp_user, smtp_pass]):
        logger.warning("SMTP not configured — skipping welcome email.")
        return
    subject = "Welcome to SurveyMatrix 🎉"
    html = f"""
    <div style="font-family:sans-serif;background:#f8fafc;padding:40px 0">
      <div style="max-width:560px;margin:0 auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08)">
        <div style="background:linear-gradient(135deg,#0d9488,#f59e0b);padding:32px;text-align:center">
          <h1 style="color:#fff;margin:0;font-size:22px">SurveyMatrix</h1>
        </div>
        <div style="padding:32px">
          <h2 style="color:#0f172a">Welcome, {full_name or username}! 👋</h2>
          <p style="color:#64748b">Your account is ready. Here are your login credentials:</p>
          <div style="background:#f0fdfa;border:1px solid #99f6e4;border-radius:10px;padding:16px;margin:20px 0">
            <p style="margin:4px 0"><strong>Username:</strong> {username}</p>
            <p style="margin:4px 0"><strong>Password:</strong> {password}</p>
          </div>
          <a href="{APP_URL}/login" style="display:inline-block;padding:12px 32px;background:linear-gradient(135deg,#0d9488,#0f766e);color:#fff;text-decoration:none;border-radius:10px;font-weight:700">Log in to SurveyMatrix →</a>
        </div>
        <div style="background:#f8fafc;padding:16px;text-align:center;font-size:12px;color:#94a3b8">© {datetime.utcnow().year} SurveyMatrix</div>
      </div>
    </div>"""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = smtp_user
    msg["To"]      = to_email
    msg.attach(MIMEText(html, "html"))
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as s:
            s.ehlo(); s.starttls(); s.login(smtp_user, smtp_pass)
            s.sendmail(smtp_user, to_email, msg.as_string())
    except Exception as e:
        logger.error(f"Welcome email failed: {e}")


# ── Root ──────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "SurveyMatrix API v2.0 running"}


# ── Auth ──────────────────────────────────────────────────────────────────────
@app.post("/auth/register", response_model=schemas.TokenResponse, status_code=201)
def register(payload: schemas.RegisterRequest, request: Request, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(status_code=409, detail="Username already taken.")
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=409, detail="Email already registered.")
    user = models.User(
        username=payload.username, email=payload.email,
        full_name=payload.full_name, hashed_password=auth.hash_password(payload.password), is_active=True
    )
    db.add(user); db.commit(); db.refresh(user)
    token = auth.create_access_token(data={"sub": user.username, "user_id": user.id})
    try:
        send_welcome_email(payload.email, payload.full_name, payload.username, payload.password)
    except Exception as e:
        logger.error(f"Welcome email dispatch error: {e}")
    return schemas.TokenResponse(access_token=token, token_type="bearer",
        user=schemas.UserOut(id=user.id, username=user.username, full_name=user.full_name))


@app.post("/auth/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == payload.username).first()
    if not user or not auth.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    token = auth.create_access_token(data={"sub": user.username, "user_id": user.id})
    return schemas.TokenResponse(access_token=token, token_type="bearer",
        user=schemas.UserOut(id=user.id, username=user.username, full_name=user.full_name))


@app.get("/auth/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(auth.get_current_user)):
    return schemas.UserOut(id=current_user.id, username=current_user.username, full_name=current_user.full_name)


@app.patch("/auth/me", response_model=schemas.UserOut)
def update_me(payload: dict, db: Session = Depends(get_db),
             current_user: models.User = Depends(auth.get_current_user)):
    # Intentionally narrow: only display name is editable here. Username/password
    # changes are out of scope so this can never affect login.
    full_name = payload.get("full_name")
    if full_name is not None:
        current_user.full_name = full_name.strip() or None
        db.commit(); db.refresh(current_user)
    return schemas.UserOut(id=current_user.id, username=current_user.username, full_name=current_user.full_name)


# ── Surveys (owner only) ──────────────────────────────────────────────────────
@app.post("/surveys", response_model=schemas.SurveyOut, status_code=201)
def create_survey(payload: schemas.SurveyCreate, db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    survey = models.Survey(
        owner_id=current_user.id, title=payload.title,
        description=payload.description, status=payload.status,
        requires_invite=payload.requires_invite
    )
    db.add(survey); db.flush()

    for i, q in enumerate(payload.questions or []):
        question = models.Question(
            survey_id=survey.id, order=q.order or i, type=q.type, text=q.text,
            required=q.required, options=q.options, logic=q.logic,
            min_rating=q.min_rating, max_rating=q.max_rating
        )
        db.add(question)

    db.flush()

    # Generate QR code for the public survey URL
    public_url = f"{APP_URL}/survey/respond/{survey.id}"
    survey.qr_code = generate_qr_code(public_url)

    db.commit(); db.refresh(survey)

    resp_count = db.query(models.Response).filter(models.Response.survey_id == survey.id).count()
    out = schemas.SurveyOut.model_validate(survey)
    out.response_count = resp_count
    return out


@app.get("/surveys", response_model=list[schemas.SurveyListItem])
def list_surveys(db: Session = Depends(get_db),
                 current_user: models.User = Depends(auth.get_current_user)):
    surveys = db.query(models.Survey).filter(
        models.Survey.owner_id == current_user.id
    ).order_by(models.Survey.created_at.desc()).all()

    result = []
    for s in surveys:
        count = db.query(models.Response).filter(models.Response.survey_id == s.id).count()
        avg   = db.query(models.Response).filter(models.Response.survey_id == s.id).all()
        rate  = sum(r.completion_pct for r in avg) / max(len(avg), 1) if avg else 0
        item  = schemas.SurveyListItem(
            id=s.id, title=s.title, status=s.status,
            created_at=s.created_at, response_count=count,
            completion_rate=round(rate, 1), qr_code=s.qr_code
        )
        result.append(item)
    return result


@app.get("/surveys/{survey_id}", response_model=schemas.SurveyOut)
def get_survey(survey_id: int, db: Session = Depends(get_db),
               current_user: models.User = Depends(auth.get_current_user)):
    survey = db.query(models.Survey).options(joinedload(models.Survey.questions)).filter(
        models.Survey.id == survey_id,
        models.Survey.owner_id == current_user.id
    ).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found.")
    count = db.query(models.Response).filter(models.Response.survey_id == survey_id).count()
    out = schemas.SurveyOut.model_validate(survey)
    out.response_count = count
    return out


@app.put("/surveys/{survey_id}", response_model=schemas.SurveyOut)
def update_survey(survey_id: int, payload: schemas.SurveyUpdate,
                  db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    survey = db.query(models.Survey).filter(
        models.Survey.id == survey_id, models.Survey.owner_id == current_user.id
    ).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found.")

    if payload.title       is not None: survey.title       = payload.title
    if payload.description is not None: survey.description = payload.description
    if payload.status      is not None: survey.status      = payload.status
    if payload.requires_invite is not None: survey.requires_invite = payload.requires_invite

    if payload.questions is not None:
        db.query(models.Question).filter(models.Question.survey_id == survey_id).delete()
        for i, q in enumerate(payload.questions):
            question = models.Question(
                survey_id=survey.id, order=q.order or i, type=q.type, text=q.text,
                required=q.required, options=q.options, logic=q.logic,
                min_rating=q.min_rating, max_rating=q.max_rating
            )
            db.add(question)

    db.commit(); db.refresh(survey)
    return schemas.SurveyOut.model_validate(survey)


@app.delete("/surveys/{survey_id}", status_code=204)
def delete_survey(survey_id: int, db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    survey = db.query(models.Survey).filter(
        models.Survey.id == survey_id, models.Survey.owner_id == current_user.id
    ).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found.")
    db.delete(survey); db.commit()


# ── Invites (bulk unique respondent links, owner only) ────────────────────────
def _survey_or_404(survey_id, db, current_user):
    survey = db.query(models.Survey).filter(
        models.Survey.id == survey_id, models.Survey.owner_id == current_user.id
    ).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found.")
    return survey


def _invite_link(survey_id: int, token: str) -> str:
    return f"{APP_URL}/survey/respond/{survey_id}?token={token}"


@app.post("/surveys/{survey_id}/invites/upload", response_model=schemas.InviteUploadResult, status_code=201)
def upload_invites_csv(survey_id: int, file: UploadFile = File(...),
                       db: Session = Depends(get_db),
                       current_user: models.User = Depends(auth.get_current_user)):
    """
    Accepts a CSV with 'name' and/or 'email' columns (case-insensitive; also
    accepts 'full_name'/'Full Name'). Generates one unique respondent link per
    row. Marks the survey as requiring an invite token to respond.
    """
    survey = _survey_or_404(survey_id, db, current_user)

    raw = file.file.read()
    try:
        text_content = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text_content = raw.decode("latin-1")

    reader = csv.DictReader(io.StringIO(text_content))
    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV file is empty or has no header row.")

    field_map = {f.strip().lower(): f for f in reader.fieldnames}
    name_field  = field_map.get("name") or field_map.get("full_name") or field_map.get("full name")
    email_field = field_map.get("email") or field_map.get("e-mail")

    created, skipped = [], 0
    for row in reader:
        name  = (row.get(name_field)  or "").strip() if name_field  else ""
        email = (row.get(email_field) or "").strip() if email_field else ""
        if not name and not email:
            skipped += 1
            continue
        invite = models.Invite(
            survey_id=survey_id,
            token=secrets.token_urlsafe(12),
            name=name or None,
            email=email or None,
            status="pending",
        )
        db.add(invite)
        created.append(invite)

    if not created:
        raise HTTPException(status_code=400, detail="No valid rows found. Include a 'name' and/or 'email' column.")

    survey.requires_invite = True
    db.commit()
    for inv in created:
        db.refresh(inv)

    out = [
        schemas.InviteOut(
            id=inv.id, token=inv.token, name=inv.name, email=inv.email,
            status=inv.status, created_at=inv.created_at,
            link=_invite_link(survey_id, inv.token),
        )
        for inv in created
    ]
    return schemas.InviteUploadResult(created=len(created), skipped=skipped, invites=out)


@app.get("/surveys/{survey_id}/invites", response_model=list[schemas.InviteOut])
def list_invites(survey_id: int, db: Session = Depends(get_db),
                 current_user: models.User = Depends(auth.get_current_user)):
    _survey_or_404(survey_id, db, current_user)
    invites = db.query(models.Invite).filter(
        models.Invite.survey_id == survey_id
    ).order_by(models.Invite.created_at.desc()).all()
    return [
        schemas.InviteOut(
            id=inv.id, token=inv.token, name=inv.name, email=inv.email,
            status=inv.status, created_at=inv.created_at,
            link=_invite_link(survey_id, inv.token),
        )
        for inv in invites
    ]


@app.get("/surveys/{survey_id}/invites/{invite_id}/qr")
def get_invite_qr(survey_id: int, invite_id: int, db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    _survey_or_404(survey_id, db, current_user)
    invite = db.query(models.Invite).filter(
        models.Invite.id == invite_id, models.Invite.survey_id == survey_id
    ).first()
    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found.")
    return {"qr_code": generate_qr_code(_invite_link(survey_id, invite.token))}


@app.delete("/surveys/{survey_id}/invites", status_code=204)
def clear_invites(survey_id: int, db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    survey = _survey_or_404(survey_id, db, current_user)
    db.query(models.Invite).filter(models.Invite.survey_id == survey_id).delete()
    survey.requires_invite = False
    db.commit()


@app.get("/surveys/{survey_id}/invites/export")
def export_invites_csv(survey_id: int, db: Session = Depends(get_db),
                       current_user: models.User = Depends(auth.get_current_user)):
    survey = _survey_or_404(survey_id, db, current_user)
    invites = db.query(models.Invite).filter(models.Invite.survey_id == survey_id).all()

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Name", "Email", "Status", "Unique Link"])
    for inv in invites:
        writer.writerow([inv.name or "", inv.email or "", inv.status, _invite_link(survey_id, inv.token)])

    return StreamingResponse(
        io.BytesIO(buf.getvalue().encode("utf-8")),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{survey.title}_invite_links.csv"'}
    )


# ── Public survey (no auth required — respondents) ────────────────────────────
@app.get("/public/survey/{survey_id}", response_model=schemas.SurveyOut)
def get_public_survey(survey_id: int, token: Optional[str] = None, db: Session = Depends(get_db)):
    survey = db.query(models.Survey).options(joinedload(models.Survey.questions)).filter(
        models.Survey.id == survey_id, models.Survey.status == "active"
    ).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found or not active.")

    if survey.requires_invite:
        if not token:
            raise HTTPException(status_code=403, detail="This survey requires a personal invite link.")
        invite = db.query(models.Invite).filter(
            models.Invite.survey_id == survey_id, models.Invite.token == token
        ).first()
        if not invite:
            raise HTTPException(status_code=403, detail="Invalid or expired invite link.")
        if invite.status == "completed":
            raise HTTPException(status_code=409, detail="This invite link has already been used to respond.")
        if invite.status == "pending":
            invite.status = "opened"
            invite.opened_at = datetime.utcnow()
            db.commit()

    return schemas.SurveyOut.model_validate(survey)


@app.post("/public/survey/{survey_id}/respond", status_code=201)
def submit_response(survey_id: int, payload: schemas.ResponseSubmit,
                    request: Request, db: Session = Depends(get_db)):
    survey = db.query(models.Survey).filter(
        models.Survey.id == survey_id, models.Survey.status == "active"
    ).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found or closed.")

    invite = None
    if survey.requires_invite:
        if not payload.token:
            raise HTTPException(status_code=403, detail="This survey requires a personal invite link.")
        invite = db.query(models.Invite).filter(
            models.Invite.survey_id == survey_id, models.Invite.token == payload.token
        ).first()
        if not invite:
            raise HTTPException(status_code=403, detail="Invalid or expired invite link.")
        if invite.status == "completed":
            raise HTTPException(status_code=409, detail="This invite link has already been used to respond.")

    total_q    = db.query(models.Question).filter(models.Question.survey_id == survey_id).count()
    answered_q = len([a for a in payload.answers if a.value or a.values])
    completion = (answered_q / total_q * 100) if total_q > 0 else 100.0

    response = models.Response(
        survey_id=survey_id,
        respondent_name=payload.respondent_name or (invite.name if invite else None),
        respondent_email=payload.respondent_email or (invite.email if invite else None),
        ip_address=request.client.host if request.client else None,
        completion_pct=completion,
        invite_id=invite.id if invite else None
    )
    db.add(response); db.flush()

    for ans in payload.answers:
        answer = models.Answer(
            response_id=response.id,
            question_id=ans.question_id,
            value=ans.value,
            values=ans.values
        )
        db.add(answer)

    if invite:
        invite.status = "completed"
        invite.completed_at = datetime.utcnow()

    db.commit()
    return {"message": "Response submitted successfully.", "response_id": response.id}


# ── Results & stats (owner only) ──────────────────────────────────────────────
@app.get("/surveys/{survey_id}/responses", response_model=list[schemas.ResponseOut])
def get_responses(survey_id: int, db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    survey = db.query(models.Survey).filter(
        models.Survey.id == survey_id, models.Survey.owner_id == current_user.id
    ).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found.")
    responses = db.query(models.Response).options(
        joinedload(models.Response.answers)
    ).filter(models.Response.survey_id == survey_id).order_by(
        models.Response.submitted_at.desc()
    ).all()
    return [schemas.ResponseOut.model_validate(r) for r in responses]


@app.get("/surveys/{survey_id}/stats")
def get_survey_stats(survey_id: int, db: Session = Depends(get_db),
                     current_user: models.User = Depends(auth.get_current_user)):
    survey = db.query(models.Survey).options(
        joinedload(models.Survey.questions)
    ).filter(models.Survey.id == survey_id, models.Survey.owner_id == current_user.id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found.")

    responses = db.query(models.Response).options(
        joinedload(models.Response.answers)
    ).filter(models.Response.survey_id == survey_id).all()

    today = datetime.utcnow().date()
    responses_today = sum(1 for r in responses if r.submitted_at.date() == today)
    avg_completion  = sum(r.completion_pct for r in responses) / max(len(responses), 1)

    q_stats = []
    for question in survey.questions:
        vals = []
        for resp in responses:
            for ans in resp.answers:
                if ans.question_id == question.id:
                    if ans.values: vals.extend(ans.values)
                    elif ans.value: vals.append(ans.value)
        counts = dict(Counter(vals))
        q_stats.append({
            "question_id": question.id,
            "question_text": question.text,
            "type": question.type,
            "total_answers": len(vals),
            "value_counts": counts,
            "average": (sum(float(v) for v in vals if v and str(v).replace('.','').isdigit()) / max(len(vals),1))
                        if question.type == "rating" else None
        })

    return {
        "total_responses": len(responses),
        "completion_rate": round(avg_completion, 1),
        "responses_today": responses_today,
        "question_stats":  q_stats
    }


# ── Dashboard stats (all surveys for logged-in user) ─────────────────────────
@app.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db),
                        current_user: models.User = Depends(auth.get_current_user)):
    surveys = db.query(models.Survey).filter(
        models.Survey.owner_id == current_user.id
    ).all()

    survey_ids    = [s.id for s in surveys]
    all_responses = db.query(models.Response).filter(
        models.Response.survey_id.in_(survey_ids)
    ).all() if survey_ids else []

    today = datetime.utcnow().date()
    responses_today = sum(1 for r in all_responses if r.submitted_at.date() == today)
    avg_completion  = sum(r.completion_pct for r in all_responses) / max(len(all_responses), 1)

    survey_list = []
    for s in surveys:
        count = sum(1 for r in all_responses if r.survey_id == s.id)
        resps = [r for r in all_responses if r.survey_id == s.id]
        rate  = sum(r.completion_pct for r in resps) / max(len(resps), 1) if resps else 0
        survey_list.append({
            "id": s.id, "title": s.title, "status": s.status,
            "responses": count, "completion": round(rate, 1)
        })

    return {
        "total_surveys":    len(surveys),
        "active_surveys":   sum(1 for s in surveys if s.status == "active"),
        "responses_today":  responses_today,
        "completion_rate":  round(avg_completion, 1),
        "surveys":          survey_list
    }


# ── Exports ───────────────────────────────────────────────────────────────────
def _get_export_data(survey_id, db, current_user):
    survey = db.query(models.Survey).options(
        joinedload(models.Survey.questions)
    ).filter(models.Survey.id == survey_id, models.Survey.owner_id == current_user.id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found.")
    responses = db.query(models.Response).options(
        joinedload(models.Response.answers)
    ).filter(models.Response.survey_id == survey_id).all()
    return survey, responses, survey.questions


@app.get("/surveys/{survey_id}/export/excel")
def export_excel(survey_id: int, db: Session = Depends(get_db),
                 current_user: models.User = Depends(auth.get_current_user)):
    survey, responses, questions = _get_export_data(survey_id, db, current_user)
    data = export_to_excel(survey, responses, questions)
    return StreamingResponse(
        io.BytesIO(data),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{survey.title}_results.xlsx"'}
    )


@app.get("/surveys/{survey_id}/export/pptx")
def export_pptx(survey_id: int, db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    survey, responses, questions = _get_export_data(survey_id, db, current_user)
    data = export_to_pptx(survey, responses, questions)
    return StreamingResponse(
        io.BytesIO(data),
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": f'attachment; filename="{survey.title}_results.pptx"'}
    )


@app.get("/surveys/{survey_id}/export/pdf")
def export_pdf(survey_id: int, db: Session = Depends(get_db),
               current_user: models.User = Depends(auth.get_current_user)):
    survey, responses, questions = _get_export_data(survey_id, db, current_user)
    data = export_to_pdf(survey, responses, questions)
    return StreamingResponse(
        io.BytesIO(data),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{survey.title}_results.pdf"'}
    )