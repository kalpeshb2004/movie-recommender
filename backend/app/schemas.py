from pydantic import BaseModel, EmailStr


class SignupIn(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginIn(BaseModel):
    email: str
    password: str