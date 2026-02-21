from fastapi import APIRouter

from app.api.deps import CurrentUser

from app import crud

router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/health-check")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/debug-seed")
def debug_seed() -> dict[str, int]:
    return {
        "users": len(crud.list_all_users()),
        "items": len(crud.list_all_items()),
    }
    


@router.get("/whoami")
def who_am_i(current_user: CurrentUser) -> dict[str, str]:
    return {"email": current_user.email}