from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.core.security import get_password_hash, verify_password
from app.models import User, UserCreate, UserUpdate, UserUpdateMe
from app.repositories import get_user_repository


def get_user_by_email(*, email: str) -> User | None:
    return get_user_repository().get_by_email(email)


def get_user(*, user_id: UUID) -> User | None:
    return get_user_repository().get(user_id)


def get_users(*, skip: int = 0, limit: int = 100) -> tuple[list[User], int]:
    return get_user_repository().list(skip=skip, limit=limit)


def create_user(*, user_create: UserCreate) -> User:
    user = User(
        id=uuid4(),
        email=user_create.email,
        full_name=user_create.full_name,
        is_active=user_create.is_active,
        is_superuser=user_create.is_superuser,
        hashed_password=get_password_hash(user_create.password),
        created_at=datetime.now(UTC),
    )
    return get_user_repository().create(user)


def update_user(*, user: User, user_update: UserUpdate) -> User:
    update_data = user_update.model_dump(exclude_unset=True)

    if "email" in update_data and update_data["email"] is not None:
        user.email = update_data["email"]
    if "full_name" in update_data:
        user.full_name = update_data["full_name"]
    if "is_active" in update_data and update_data["is_active"] is not None:
        user.is_active = update_data["is_active"]
    if "is_superuser" in update_data and update_data["is_superuser"] is not None:
        user.is_superuser = update_data["is_superuser"]
    if "password" in update_data and update_data["password"]:
        user.hashed_password = get_password_hash(update_data["password"])

    return get_user_repository().update(user)


def update_user_me(*, user: User, user_update: UserUpdateMe) -> User:
    update_data = user_update.model_dump(exclude_unset=True)

    if "email" in update_data and update_data["email"] is not None:
        user.email = update_data["email"]
    if "full_name" in update_data:
        user.full_name = update_data["full_name"]

    return get_user_repository().update(user)


def update_user_password(*, user: User, new_password: str) -> User:
    user.hashed_password = get_password_hash(new_password)
    return get_user_repository().update(user)


def delete_user(*, user: User, cascade_items: bool = True) -> None:
    get_user_repository().delete(user_id=user.id, cascade_items=cascade_items)


def authenticate(*, email: str, password: str) -> User | None:
    user = get_user_by_email(email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def list_all_users() -> list[User]:
    return get_user_repository().list_all()
