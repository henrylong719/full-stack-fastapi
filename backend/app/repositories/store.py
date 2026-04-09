from dataclasses import dataclass

from app.db.mysql import mysql_database
from app.repositories.interfaces import ItemRepository, UserRepository
from app.repositories.mysql.items import MySQLItemRepository
from app.repositories.mysql.users import MySQLUserRepository


@dataclass(frozen=True, slots=True)
class RepositoryBundle:
    users: UserRepository
    items: ItemRepository


_mysql_bundle = RepositoryBundle(
    users=MySQLUserRepository(mysql_database),
    items=MySQLItemRepository(mysql_database),
)


def get_repositories() -> RepositoryBundle:
    return _mysql_bundle


def get_user_repository() -> UserRepository:
    return get_repositories().users


def get_item_repository() -> ItemRepository:
    return get_repositories().items


def initialize_repositories() -> None:
    mysql_database.initialize()


def reset_repositories() -> None:
    mysql_database.initialize()
    mysql_database.reset_data()
