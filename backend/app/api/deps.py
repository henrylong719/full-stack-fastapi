import secrets
from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Cookie, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from app import crud
from app.core.config import settings
from app.core.security import ALGORITHM
from app.models import TokenPayload, User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token",
    auto_error=False,
)

BearerTokenDep = Annotated[str | None, Depends(reusable_oauth2)]
CookieTokenDep = Annotated[
    str | None, Cookie(alias=settings.ACCESS_TOKEN_COOKIE_NAME)
]

SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


def get_current_user(
    request: Request,
    bearer_token: BearerTokenDep,
    cookie_token: CookieTokenDep = None,
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = bearer_token or cookie_token
    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except jwt.PyJWTError:
        raise credentials_exception from None

    if token_data.sub is None:
        raise credentials_exception

    try:
        user_id = UUID(token_data.sub)
    except ValueError:
        raise credentials_exception from None

    user = crud.get_user(user_id=user_id)
    if not user:
        raise credentials_exception

    if token_data.session_version != user.session_version:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    if cookie_token and not bearer_token and request.method not in SAFE_METHODS:
        csrf_header = request.headers.get("X-CSRF-Token")
        if (
            not token_data.csrf
            or not csrf_header
            or not secrets.compare_digest(csrf_header, token_data.csrf)
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid CSRF token",
            )

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user


CurrentSuperuser = Annotated[User, Depends(get_current_active_superuser)]
