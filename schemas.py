# # # from typing import Optional

# # # from pydantic import BaseModel, Field


# # # class LoginRequest(BaseModel):
# # #     username: str = Field(..., min_length=1)
# # #     password: str = Field(..., min_length=1)


# # # class UserOut(BaseModel):
# # #     id: int
# # #     username: str
# # #     full_name: Optional[str] = None

# # #     class Config:
# # #         from_attributes = True


# # # class TokenResponse(BaseModel):
# # #     access_token: str
# # #     token_type: str
# # #     user: UserOut


# # from typing import Optional
# # from pydantic import BaseModel, Field


# # class LoginRequest(BaseModel):
# #     username: str = Field(..., min_length=1)
# #     password: str = Field(..., min_length=1)


# # class UserOut(BaseModel):
# #     id: int
# #     username: str
# #     full_name: Optional[str] = None

# #     model_config = {"from_attributes": True}


# # class TokenResponse(BaseModel):
# #     access_token: str
# #     token_type: str
# #     user: UserOut


# from typing import Optional
# from pydantic import BaseModel, EmailStr, field_validator
# import re


# # ── Auth ──────────────────────────────────────────────────────────────────────

# class LoginRequest(BaseModel):
#     username: str
#     password: str


# class RegisterRequest(BaseModel):
#     full_name: str
#     username: str
#     email: EmailStr
#     password: str

#     @field_validator("username")
#     @classmethod
#     def username_alphanumeric(cls, v):
#         if not re.match(r"^[a-zA-Z0-9_]{3,50}$", v):
#             raise ValueError("Username must be 3–50 characters: letters, numbers, underscores only.")
#         return v.lower()

#     @field_validator("password")
#     @classmethod
#     def password_strength(cls, v):
#         if len(v) < 6:
#             raise ValueError("Password must be at least 6 characters.")
#         return v


# # ── User ──────────────────────────────────────────────────────────────────────

# class UserOut(BaseModel):
#     id: int
#     username: str
#     full_name: Optional[str] = None

#     class Config:
#         from_attributes = True


# # ── Token ─────────────────────────────────────────────────────────────────────

# class TokenResponse(BaseModel):
#     access_token: str
#     token_type: str
#     user: UserOut


from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
import re


# ── Auth ──────────────────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v):
        if not re.match(r"^[a-zA-Z0-9_]{3,50}$", v):
            raise ValueError("Username must be 3–50 chars: letters, numbers, underscores.")
        return v.lower()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters.")
        return v

class UserOut(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOut


# ── Questions ─────────────────────────────────────────────────────────────────
class QuestionCreate(BaseModel):
    order: int = 0
    type: str                           # text|textarea|multiple_choice|checkbox|rating|dropdown|file|date
    text: str
    required: bool = False
    options: Optional[List[str]] = None
    logic: Optional[dict] = None
    min_rating: Optional[int] = None
    max_rating: Optional[int] = None

class QuestionOut(QuestionCreate):
    id: int
    survey_id: int
    class Config:
        from_attributes = True


# ── Surveys ───────────────────────────────────────────────────────────────────
class SurveyCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "draft"
    requires_invite: bool = False
    questions: Optional[List[QuestionCreate]] = []

class SurveyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    requires_invite: Optional[bool] = None
    questions: Optional[List[QuestionCreate]] = None

class SurveyOut(BaseModel):
    id: int
    owner_id: int
    title: str
    description: Optional[str] = None
    status: str
    qr_code: Optional[str] = None
    requires_invite: Optional[bool] = False
    created_at: datetime
    questions: List[QuestionOut] = []
    response_count: Optional[int] = 0
    completion_rate: Optional[float] = 0.0
    class Config:
        from_attributes = True

class SurveyListItem(BaseModel):
    id: int
    title: str
    status: str
    created_at: datetime
    response_count: int = 0
    completion_rate: float = 0.0
    qr_code: Optional[str] = None
    class Config:
        from_attributes = True


# ── Responses ─────────────────────────────────────────────────────────────────
class AnswerSubmit(BaseModel):
    question_id: int
    value: Optional[str] = None
    values: Optional[List[str]] = None

class ResponseSubmit(BaseModel):
    respondent_name: Optional[str] = None
    respondent_email: Optional[str] = None
    token: Optional[str] = None
    answers: List[AnswerSubmit]

class AnswerOut(BaseModel):
    id: int
    question_id: int
    value: Optional[str] = None
    values: Optional[List[str]] = None
    class Config:
        from_attributes = True

class ResponseOut(BaseModel):
    id: int
    survey_id: int
    respondent_name: Optional[str] = None
    respondent_email: Optional[str] = None
    submitted_at: datetime
    completion_pct: float
    answers: List[AnswerOut] = []
    class Config:
        from_attributes = True


# ── Stats ─────────────────────────────────────────────────────────────────────
class SurveyStats(BaseModel):
    total_responses: int
    completion_rate: float
    responses_today: int
    question_stats: List[dict]


# ── Invites (bulk unique respondent links) ─────────────────────────────────────
class InviteOut(BaseModel):
    id: int
    token: str
    name: Optional[str] = None
    email: Optional[str] = None
    status: str
    created_at: datetime
    link: Optional[str] = None
    class Config:
        from_attributes = True

class InviteUploadResult(BaseModel):
    created: int
    skipped: int
    invites: List[InviteOut]


# ── Public contact form ─────────────────────────────────────────────────────────
class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str