from typing import Optional
from uuid import UUID

from app.database import get_db
from app.models.auth import UserRecord


def get_user_by_id(user_id: UUID) -> Optional[UserRecord]:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, tenant_id, email, role FROM users WHERE id = %s",
                (str(user_id),),
            )
            row = cur.fetchone()
            if not row:
                return None
            return UserRecord(**row)


def get_user_by_email(email: str) -> Optional[UserRecord]:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, tenant_id, email, role FROM users WHERE email = %s",
                (email.lower(),),
            )
            row = cur.fetchone()
            if not row:
                return None
            return UserRecord(**row)
