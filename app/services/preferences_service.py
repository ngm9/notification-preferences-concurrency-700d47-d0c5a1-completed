from uuid import UUID

from fastapi import HTTPException

from app.models.auth import TokenClaims
from app.models.preferences import (
    NotificationPreferences,
    PreferencesCreateRequest,
    PreferencesUpdateRequest,
)
from app.repositories.preferences_repository import (
    create_preferences as insert_preferences,
    get_preferences_by_user,
    update_preferences,
)
from app.repositories.user_repository import get_user_by_id
from app.services.access_control import authorize_preferences_access
from app.services.etag import parse_etag_version


def _require_user(user_id: UUID):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def fetch_user_preferences(
    user_id: UUID,
    claims: TokenClaims,
) -> NotificationPreferences:
    user = _require_user(user_id)
    authorize_preferences_access(claims, user_id, user.tenant_id)

    prefs = get_preferences_by_user(user_id)
    if not prefs:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return prefs


def apply_preference_updates(
    user_id: UUID,
    request: PreferencesUpdateRequest,
    claims: TokenClaims,
    if_match: str | None,
) -> NotificationPreferences:
    if not if_match:
        raise HTTPException(status_code=428, detail="If-Match header required")

    user = _require_user(user_id)
    authorize_preferences_access(claims, user_id, user.tenant_id)

    try:
        expected_version = parse_etag_version(if_match)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid If-Match header") from exc

    updates = request.model_dump(exclude_none=True)
    if not updates:
        prefs = get_preferences_by_user(user_id)
        if not prefs:
            raise HTTPException(status_code=404, detail="Preferences not found")
        return prefs

    updated = update_preferences(user_id, updates, expected_version)
    if not updated:
        existing = get_preferences_by_user(user_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Preferences not found")
        raise HTTPException(status_code=412, detail="Preferences version mismatch")
    return updated


def create_user_preferences(
    user_id: UUID,
    request: PreferencesCreateRequest,
    claims: TokenClaims,
) -> NotificationPreferences:
    user = _require_user(user_id)
    authorize_preferences_access(claims, user_id, user.tenant_id)

    if get_preferences_by_user(user_id):
        raise HTTPException(status_code=409, detail="Preferences already exist")

    values = request.model_dump()
    return insert_preferences(user_id, user.tenant_id, values)
