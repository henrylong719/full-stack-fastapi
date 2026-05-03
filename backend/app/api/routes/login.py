from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import CurrentUser
from app.models import Message, Token, UserPublic
from app.services.auth import login_with_password, logout_session

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/access-token")
def login_access_token(
    request: Request,
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    return login_with_password(
        request=request,
        response=response,
        email=form_data.username,
        password=form_data.password,
    )


@router.post("/logout")
def logout(response: Response) -> Message:
    logout_session(response)
    return Message(message="Logged out successfully")


@router.post("/test-token")
def test_token(current_user: CurrentUser) -> UserPublic:
    return UserPublic.model_validate(current_user)
