import secrets
from datetime import timedelta

from fastapi import HTTPException, Request, Response, status

from app import crud
from app.core.config import settings
from app.core.cookies import clear_auth_cookies, set_auth_cookies
from app.core.security import create_access_token
from app.models import Token, User
from app.services.login_rate_limit import (
    check_login_rate_limit,
    clear_failed_logins,
    get_login_key,
    record_failed_login,
)


def authenticate_login(*, email: str, password: str, login_key: str) -> User:
    user = crud.authenticate(email=email, password=password)
    if not user:
        record_failed_login(login_key)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        record_failed_login(login_key)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return user


def create_login_session(response: Response, user: User) -> Token:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    csrf_token = secrets.token_urlsafe(32)
    access_token = create_access_token(
        subject=user.id,
        expires_delta=access_token_expires,
        session_version=user.session_version,
        csrf_token=csrf_token,
    )
    set_auth_cookies(
        response,
        access_token=access_token,
        csrf_token=csrf_token,
        max_age_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return Token(access_token=access_token)


def login_with_password(
    *,
    request: Request,
    response: Response,
    email: str,
    password: str,
) -> Token:
    login_key = get_login_key(request, email)
    check_login_rate_limit(login_key)
    user = authenticate_login(email=email, password=password, login_key=login_key)
    token = create_login_session(response, user)
    clear_failed_logins(login_key)
    return token


def logout_session(response: Response) -> None:
    clear_auth_cookies(response)
