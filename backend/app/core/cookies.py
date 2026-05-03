from fastapi import Response

from app.core.config import settings


def set_auth_cookies(
    response: Response,
    *,
    access_token: str,
    csrf_token: str,
    max_age_seconds: int,
) -> None:
    secure_cookie = not settings.is_local
    response.set_cookie(
        key=settings.ACCESS_TOKEN_COOKIE_NAME,
        value=access_token,
        max_age=max_age_seconds,
        path="/",
        domain=settings.COOKIE_DOMAIN,
        secure=secure_cookie,
        httponly=True,
        samesite="lax",
    )
    response.set_cookie(
        key=settings.CSRF_COOKIE_NAME,
        value=csrf_token,
        max_age=max_age_seconds,
        path="/",
        domain=settings.COOKIE_DOMAIN,
        secure=secure_cookie,
        httponly=False,
        samesite="lax",
    )


def clear_auth_cookies(response: Response) -> None:
    secure_cookie = not settings.is_local
    response.delete_cookie(
        key=settings.ACCESS_TOKEN_COOKIE_NAME,
        path="/",
        domain=settings.COOKIE_DOMAIN,
        secure=secure_cookie,
        httponly=True,
        samesite="lax",
    )
    response.delete_cookie(
        key=settings.CSRF_COOKIE_NAME,
        path="/",
        domain=settings.COOKIE_DOMAIN,
        secure=secure_cookie,
        httponly=False,
        samesite="lax",
    )
