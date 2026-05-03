import secrets
from collections import defaultdict, deque
from datetime import timedelta
from time import monotonic
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.deps import CurrentUser
from app.core.config import settings
from app.core.security import create_access_token
from app.models import Message, Token, UserPublic

router = APIRouter(prefix="/login", tags=["login"])

LOGIN_WINDOW_SECONDS = 5 * 60
MAX_LOGIN_ATTEMPTS = 5
_LOGIN_ATTEMPTS: dict[str, deque[float]] = defaultdict(deque)


def _login_key(request: Request, email: str) -> str:
    client_host = request.client.host if request.client else "unknown"
    return f"{client_host}:{email.lower()}"


def _prune_attempts(attempts: deque[float], now: float) -> None:
    while attempts and now - attempts[0] > LOGIN_WINDOW_SECONDS:
        attempts.popleft()


def _check_login_rate_limit(key: str) -> None:
    now = monotonic()
    attempts = _LOGIN_ATTEMPTS[key]
    _prune_attempts(attempts, now)
    if len(attempts) >= MAX_LOGIN_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed login attempts. Please try again later.",
        )


def _record_failed_login(key: str) -> None:
    now = monotonic()
    attempts = _LOGIN_ATTEMPTS[key]
    _prune_attempts(attempts, now)
    attempts.append(now)


def _clear_failed_logins(key: str) -> None:
    _LOGIN_ATTEMPTS.pop(key, None)


def _set_auth_cookies(
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


def _clear_auth_cookies(response: Response) -> None:
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


@router.post("/access-token")
def login_access_token(
    request: Request,
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    key = _login_key(request, form_data.username)
    _check_login_rate_limit(key)

    user = crud.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        _record_failed_login(key)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        _record_failed_login(key)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    csrf_token = secrets.token_urlsafe(32)
    access_token = create_access_token(
        subject=user.id,
        expires_delta=access_token_expires,
        session_version=user.session_version,
        csrf_token=csrf_token,
    )
    _set_auth_cookies(
        response,
        access_token=access_token,
        csrf_token=csrf_token,
        max_age_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    _clear_failed_logins(key)
    return Token(access_token=access_token)


@router.post("/logout")
def logout(response: Response) -> Message:
    _clear_auth_cookies(response)
    return Message(message="Logged out successfully")


@router.post("/test-token")
def test_token(current_user: CurrentUser) -> UserPublic:
    return UserPublic.model_validate(current_user)
