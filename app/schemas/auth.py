from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "doctor"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str