from uuid import UUID

from fastapi import APIRouter, Depends, Header, Response

from app.middleware.auth import decode_token
from app.models.auth import TokenClaims
from app.models.preferences import (
    PreferencesCreateRequest,
    PreferencesUpdateRequest,
    PreferencesResponse,
)
from app.services.etag import format_etag
from app.services.preferences_service import (
    apply_preference_updates,
    create_user_preferences,
    fetch_user_preferences,
)

router = APIRouter()


@router.get("/users/{user_id}/preferences", response_model=PreferencesResponse)
def get_preferences(
    user_id: UUID,
    response: Response,
    claims: TokenClaims = Depends(decode_token),
):
    prefs = fetch_user_preferences(user_id, claims)
    response.headers["etag"] = format_etag(prefs.version)
    return PreferencesResponse(**prefs.model_dump())


@router.post("/users/{user_id}/preferences", response_model=PreferencesResponse, status_code=201)
def create_preferences(
    user_id: UUID,
    body: PreferencesCreateRequest,
    claims: TokenClaims = Depends(decode_token),
):
    prefs = create_user_preferences(user_id, body, claims)
    return PreferencesResponse(**prefs.model_dump())


@router.put("/users/{user_id}/preferences", response_model=PreferencesResponse)
def update_preferences(
    user_id: UUID,
    body: PreferencesUpdateRequest,
    claims: TokenClaims = Depends(decode_token),
    if_match: str | None = Header(default=None, alias="If-Match"),
):
    updated = apply_preference_updates(user_id, body, claims, if_match)
    return PreferencesResponse(**updated.model_dump())
