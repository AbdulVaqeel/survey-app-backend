# from pydantic import BaseModel
# from typing import Optional


# class LoginRequest(BaseModel):
#     username: str
#     password: str


# class UserOut(BaseModel):
#     id: int
#     username: str
#     full_name: Optional[str] = None

#     class Config:
#         from_attributes = True


# class TokenResponse(BaseModel):
#     access_token: str
#     token_type: str
#     user: UserOut

from typing import Optional

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


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