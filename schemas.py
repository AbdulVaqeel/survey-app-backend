# # from typing import Optional

# # from pydantic import BaseModel, Field


# # class LoginRequest(BaseModel):
# #     username: str = Field(..., min_length=1)
# #     password: str = Field(..., min_length=1)


# # class UserOut(BaseModel):
# #     id: int
# #     username: str
# #     full_name: Optional[str] = None

# #     class Config:
# #         from_attributes = True


# # class TokenResponse(BaseModel):
# #     access_token: str
# #     token_type: str
# #     user: UserOut


# from typing import Optional
# from pydantic import BaseModel, Field


# class LoginRequest(BaseModel):
#     username: str = Field(..., min_length=1)
#     password: str = Field(..., min_length=1)


# class UserOut(BaseModel):
#     id: int
#     username: str
#     full_name: Optional[str] = None

#     model_config = {"from_attributes": True}


# class TokenResponse(BaseModel):
#     access_token: str
#     token_type: str
#     user: UserOut


from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
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
            raise ValueError("Username must be 3–50 characters: letters, numbers, underscores only.")
        return v.lower()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters.")
        return v


# ── User ──────────────────────────────────────────────────────────────────────

class UserOut(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None

    class Config:
        from_attributes = True


# ── Token ─────────────────────────────────────────────────────────────────────

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOut