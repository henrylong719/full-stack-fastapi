from app.crud.items import (
    create_item,
    delete_item,
    delete_items_by_owner,
    get_item,
    get_items,
    get_items_by_owner,
    list_all_items,
    update_item,
)
from app.crud.seed import seed_mock_data
from app.crud.users import (
    authenticate,
    create_user,
    delete_user,
    get_user,
    get_user_by_email,
    get_users,
    list_all_users,
    update_user,
    update_user_me,
    update_user_password,
)
from app.repositories import initialize_repositories, reset_repositories

__all__ = [
    "authenticate",
    "create_item",
    "create_user",
    "delete_item",
    "delete_items_by_owner",
    "delete_user",
    "get_item",
    "get_items",
    "get_items_by_owner",
    "get_user",
    "get_user_by_email",
    "get_users",
    "list_all_items",
    "list_all_users",
    "reset_data_store",
    "seed_mock_data",
    "initialize_data_store",
    "update_item",
    "update_user",
    "update_user_me",
    "update_user_password",
]


def initialize_data_store() -> None:
    initialize_repositories()
    seed_mock_data()


def reset_data_store() -> None:
    reset_repositories()
    seed_mock_data()
