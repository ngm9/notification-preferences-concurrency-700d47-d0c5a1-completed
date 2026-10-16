from fastapi import APIRouter, HTTPException

from app.middleware.auth import create_access_token
from app.models.auth import LoginRequest, TokenResponse
from app.repositories.user_repository import get_user_by_email

router = APIRouter()


@router.post("/auth/login", response_model=TokenResponse)
def login(body: LoginRequest):
    user = get_user_by_email(body.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user.id, user.tenant_id, user.role)
    return TokenResponse(access_token=token)
