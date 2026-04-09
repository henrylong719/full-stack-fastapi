from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from datetime import UTC, datetime
from typing import Any, cast

import mysql.connector
from mysql.connector import pooling
from mysql.connector.connection import MySQLConnection

from app.core.config import settings
from app.db.schema import MYSQL_SCHEMA_STATEMENTS

type DBRow = Mapping[str, Any]


class MySQLDatabase:
    def __init__(self) -> None:
        self._pool: pooling.MySQLConnectionPool | None = None

    def initialize(self) -> None:
        if settings.MYSQL_AUTO_CREATE_DATABASE:
            self.ensure_database_exists()

        self._ensure_pool()

        if settings.MYSQL_AUTO_CREATE_TABLES:
            self.create_tables()

    def reset_data(self) -> None:
        self.execute("DELETE FROM items")
        self.execute("DELETE FROM users")

    def fetch_one(
        self, query: str, params: Sequence[Any] | None = None
    ) -> DBRow | None:
        with self.connection() as connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute(query, params or ())
                row = cursor.fetchone()
                return cast(DBRow | None, row)
            finally:
                cursor.close()

    def fetch_all(self, query: str, params: Sequence[Any] | None = None) -> list[DBRow]:
        with self.connection() as connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute(query, params or ())
                rows = cast(list[DBRow], cursor.fetchall())
                return rows
            finally:
                cursor.close()

    def execute(self, query: str, params: Sequence[Any] | None = None) -> int:
        with self.connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(query, params or ())
                connection.commit()
                return cursor.rowcount
            except Exception:
                connection.rollback()
                raise
            finally:
                cursor.close()

    def create_tables(self) -> None:
        with self.connection() as connection:
            cursor = connection.cursor()
            try:
                for statement in MYSQL_SCHEMA_STATEMENTS:
                    cursor.execute(statement)
                connection.commit()
            except Exception:
                connection.rollback()
                raise
            finally:
                cursor.close()

    def ensure_database_exists(self) -> None:
        database_name = self._escaped_database_name()
        connection = cast(
            MySQLConnection,
            mysql.connector.connect(
                host=settings.MYSQL_HOST,
                port=settings.MYSQL_PORT,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                connection_timeout=settings.MYSQL_CONNECT_TIMEOUT,
                use_pure=True,
            ),
        )
        try:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS `{database_name}` "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
                connection.commit()
            finally:
                cursor.close()
        finally:
            connection.close()

    @staticmethod
    def to_db_datetime(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value
        return value.astimezone(UTC).replace(tzinfo=None)

    @staticmethod
    def from_db_datetime(value: datetime | None) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is not None:
            return value.astimezone(UTC)
        return value.replace(tzinfo=UTC)

    @contextmanager
    def connection(self) -> Iterator[MySQLConnection]:
        pool = self._ensure_pool()
        connection = cast(MySQLConnection, pool.get_connection())
        try:
            yield connection
        finally:
            connection.close()

    def _ensure_pool(self) -> pooling.MySQLConnectionPool:
        if self._pool is None:
            self._pool = pooling.MySQLConnectionPool(
                pool_name=settings.MYSQL_POOL_NAME,
                pool_size=settings.MYSQL_POOL_SIZE,
                host=settings.MYSQL_HOST,
                port=settings.MYSQL_PORT,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                database=settings.MYSQL_DATABASE,
                connection_timeout=settings.MYSQL_CONNECT_TIMEOUT,
                autocommit=False,
                use_pure=True,
            )

        pool = self._pool
        if pool is None:
            raise RuntimeError("MySQL connection pool was not initialized")
        return pool

    @staticmethod
    def _escaped_database_name() -> str:
        return settings.MYSQL_DATABASE.replace("`", "``")


mysql_database = MySQLDatabase()
