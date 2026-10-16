from pydantic import BaseModel, EmailStr
from uuid import UUID


class TokenClaims(BaseModel):
    user_id: UUID
    tenant_id: UUID
    role: str


class LoginRequest(BaseModel):
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRecord(BaseModel):
    id: UUID
    tenant_id: UUID
    email: str
    role: str
