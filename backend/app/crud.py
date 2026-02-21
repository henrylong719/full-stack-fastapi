from collections.abc import Sequence
from uuid import UUID

from app.core.security import get_password_hash, verify_password
from app.models import (
    Item,
    ItemCreate,
    ItemUpdate,
    User,
    UserCreate,
    UserUpdate,
    UserUpdateMe,
)

_USERS_BY_ID: dict[UUID, User] = {}
_ITEMS_BY_ID: dict[UUID, Item] = {}


def _seed_mock_data() -> None:
    if _USERS_BY_ID:
        return

    admin = User(
        email="admin@example.com",
        full_name="Admin User",
        is_active=True,
        is_superuser=True,
        hashed_password=get_password_hash("changethis123"),
    )
    alice = User(
        email="alice@example.com",
        full_name="Alice",
        is_active=True,
        is_superuser=False,
        hashed_password=get_password_hash("password123"),
    )

    _USERS_BY_ID[admin.id] = admin
    _USERS_BY_ID[alice.id] = alice

    item1 = Item(
        title="Camping Tent",
        description="2-person tent, lightweight",
        owner_id=alice.id,
    )
    item2 = Item(
        title="Portable Stove",
        description="Small gas camping stove",
        owner_id=alice.id,
    )
    item3 = Item(
        title="Admin Test Item",
        description="Seed item owned by admin",
        owner_id=admin.id,
    )

    _ITEMS_BY_ID[item1.id] = item1
    _ITEMS_BY_ID[item2.id] = item2
    _ITEMS_BY_ID[item3.id] = item3


_seed_mock_data()


# ---------------- User CRUD ----------------


def get_user_by_email(*, email: str) -> User | None:
    return next(
        (u for u in _USERS_BY_ID.values() if u.email.lower() == email.lower()), None
    )


def get_user(*, user_id: UUID) -> User | None:
    return _USERS_BY_ID.get(user_id)


def get_users(*, skip: int = 0, limit: int = 100) -> tuple[list[User], int]:
    users = list(_USERS_BY_ID.values())
    users.sort(key=lambda u: u.created_at, reverse=True)
    total = len(users)
    return users[skip : skip + limit], total


def create_user(*, user_create: UserCreate) -> User:
    user = User(
        email=user_create.email,
        full_name=user_create.full_name,
        is_active=user_create.is_active,
        is_superuser=user_create.is_superuser,
        hashed_password=get_password_hash(user_create.password),
    )
    _USERS_BY_ID[user.id] = user
    return user


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

    _USERS_BY_ID[user.id] = user
    return user


def update_user_me(*, user: User, user_update: UserUpdateMe) -> User:
    update_data = user_update.model_dump(exclude_unset=True)

    if "email" in update_data and update_data["email"] is not None:
        user.email = update_data["email"]
    if "full_name" in update_data:
        user.full_name = update_data["full_name"]

    _USERS_BY_ID[user.id] = user
    return user


def update_user_password(*, user: User, new_password: str) -> User:
    user.hashed_password = get_password_hash(new_password)
    _USERS_BY_ID[user.id] = user
    return user


def delete_items_by_owner(*, owner_id: UUID) -> int:
    to_delete = [
        item_id for item_id, item in _ITEMS_BY_ID.items() if item.owner_id == owner_id
    ]
    for item_id in to_delete:
        _ITEMS_BY_ID.pop(item_id, None)
    return len(to_delete)


def delete_user(*, user: User, cascade_items: bool = True) -> None:
    if cascade_items:
        delete_items_by_owner(owner_id=user.id)
    _USERS_BY_ID.pop(user.id, None)


def authenticate(*, email: str, password: str) -> User | None:
    user = get_user_by_email(email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# ---------------- Item CRUD ----------------


def create_item(*, item_in: ItemCreate, owner_id: UUID) -> Item:
    item = Item(
        title=item_in.title,
        description=item_in.description,
        owner_id=owner_id,
    )
    _ITEMS_BY_ID[item.id] = item
    return item


def get_item(*, item_id: UUID) -> Item | None:
    return _ITEMS_BY_ID.get(item_id)


def get_items(*, skip: int = 0, limit: int = 100) -> tuple[list[Item], int]:
    items = list(_ITEMS_BY_ID.values())
    items.sort(key=lambda i: i.created_at, reverse=True)
    total = len(items)
    return items[skip : skip + limit], total


def get_items_by_owner(
    *, owner_id: UUID, skip: int = 0, limit: int = 100
) -> tuple[list[Item], int]:
    items = [i for i in _ITEMS_BY_ID.values() if i.owner_id == owner_id]
    items.sort(key=lambda i: i.created_at, reverse=True)
    total = len(items)
    return items[skip : skip + limit], total


def update_item(*, item: Item, item_in: ItemUpdate) -> Item:
    update_data = item_in.model_dump(exclude_unset=True)

    if "title" in update_data and update_data["title"] is not None:
        item.title = update_data["title"]
    if "description" in update_data:
        item.description = update_data["description"]

    _ITEMS_BY_ID[item.id] = item
    return item


def delete_item(*, item: Item) -> None:
    _ITEMS_BY_ID.pop(item.id, None)


# ---------------- Helpers ----------------


def reset_mock_data() -> None:
    _USERS_BY_ID.clear()
    _ITEMS_BY_ID.clear()
    _seed_mock_data()


def list_all_users() -> Sequence[User]:
    return list(_USERS_BY_ID.values())


def list_all_items() -> Sequence[Item]:
    return list(_ITEMS_BY_ID.values())
