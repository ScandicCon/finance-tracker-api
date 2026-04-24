from pydantic import BaseModel, EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str