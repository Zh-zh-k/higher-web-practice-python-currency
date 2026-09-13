from datetime import datetime

from pydantic import BaseModel, EmailStr


class LoginDTO(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenDTO(BaseModel):
    refresh_token: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class TokenPayload(BaseModel):
    user_id: int
    email: str
    exp: datetime
    token_type: str
