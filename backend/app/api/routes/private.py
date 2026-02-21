from fastapi import APIRouter, HTTPException

from app import crud
from app.core.config import settings
from app.models import Message

router = APIRouter(prefix="/private", tags=["private"])


def _ensure_local() -> None:
    # Extra guard (even though router is only mounted in local env)
    if settings.ENVIRONMENT != "local":
        raise HTTPException(status_code=404, detail="Not found")


@router.post("/reset-mock-data")
def reset_mock_data() -> Message:
    _ensure_local()
    crud.reset_mock_data()
    return Message(message="Mock data reset successfully")


@router.get("/mock-summary")
def mock_summary() -> dict:
    _ensure_local()
    users = crud.list_all_users()
    items = crud.list_all_items()

    return {
        "environment": settings.ENVIRONMENT,
        "users_count": len(users),
        "items_count": len(items),
        "users": [
            {
                "id": str(u.id),
                "email": u.email,
                "full_name": u.full_name,
                "is_active": u.is_active,
                "is_superuser": u.is_superuser,
            }
            for u in users
        ],
        "items": [
            {
                "id": str(i.id),
                "title": i.title,
                "owner_id": str(i.owner_id),
            }
            for i in items
        ],
    }


@router.get("/all-users")
def all_users() -> dict:
    _ensure_local()
    users = crud.list_all_users()
    return {
        "count": len(users),
        "data": [
            {
                "id": str(u.id),
                "email": u.email,
                "full_name": u.full_name,
                "is_active": u.is_active,
                "is_superuser": u.is_superuser,
                "created_at": u.created_at.isoformat(),
            }
            for u in users
        ],
    }


@router.get("/all-items")
def all_items() -> dict:
    _ensure_local()
    items = crud.list_all_items()
    return {
        "count": len(items),
        "data": [
            {
                "id": str(i.id),
                "title": i.title,
                "description": i.description,
                "owner_id": str(i.owner_id),
                "created_at": i.created_at.isoformat(),
            }
            for i in items
        ],
    }
