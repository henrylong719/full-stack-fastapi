from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from app.db.mysql import DBRow, MySQLDatabase
from app.models import User


class MySQLUserRepository:
    def __init__(self, database: MySQLDatabase) -> None:
        self.database = database

    def get_by_email(self, email: str) -> User | None:
        row = self.database.fetch_one(
            """
            SELECT
                id,
                email,
                full_name,
                is_active,
                is_superuser,
                hashed_password,
                created_at
            FROM users
            WHERE LOWER(email) = LOWER(%s)
            LIMIT 1
            """,
            (email,),
        )
        return self._row_to_user(row)

    def get(self, user_id: UUID) -> User | None:
        row = self.database.fetch_one(
            """
            SELECT
                id,
                email,
                full_name,
                is_active,
                is_superuser,
                hashed_password,
                created_at
            FROM users
            WHERE id = %s
            LIMIT 1
            """,
            (str(user_id),),
        )
        return self._row_to_user(row)

    def list(self, *, skip: int = 0, limit: int = 100) -> tuple[list[User], int]:
        rows = self.database.fetch_all(
            """
            SELECT
                id,
                email,
                full_name,
                is_active,
                is_superuser,
                hashed_password,
                created_at
            FROM users
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, skip),
        )
        count_row = self.database.fetch_one("SELECT COUNT(*) AS count FROM users")
        count = int(count_row["count"]) if count_row else 0
        return [self._require_user(row) for row in rows], count

    def create(self, user: User) -> User:
        self.database.execute(
            """
            INSERT INTO users (
                id,
                email,
                full_name,
                is_active,
                is_superuser,
                hashed_password,
                created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                str(user.id),
                user.email,
                user.full_name,
                user.is_active,
                user.is_superuser,
                user.hashed_password,
                self.database.to_db_datetime(user.created_at),
            ),
        )
        return user

    def update(self, user: User) -> User:
        self.database.execute(
            """
            UPDATE users
            SET email = %s,
                full_name = %s,
                is_active = %s,
                is_superuser = %s,
                hashed_password = %s
            WHERE id = %s
            """,
            (
                user.email,
                user.full_name,
                user.is_active,
                user.is_superuser,
                user.hashed_password,
                str(user.id),
            ),
        )
        return user

    def delete(self, *, user_id: UUID, cascade_items: bool = True) -> None:
        if not cascade_items:
            self.database.execute(
                "DELETE FROM items WHERE owner_id = %s",
                (str(user_id),),
            )

        self.database.execute("DELETE FROM users WHERE id = %s", (str(user_id),))

    def list_all(self) -> list[User]:
        rows = self.database.fetch_all(
            """
            SELECT
                id,
                email,
                full_name,
                is_active,
                is_superuser,
                hashed_password,
                created_at
            FROM users
            ORDER BY created_at DESC
            """
        )
        return [self._require_user(row) for row in rows]

    def _row_to_user(self, row: DBRow | None) -> User | None:
        if not row:
            return None

        return User(
            id=UUID(row["id"]),
            email=row["email"],
            full_name=row["full_name"],
            is_active=bool(row["is_active"]),
            is_superuser=bool(row["is_superuser"]),
            hashed_password=row["hashed_password"],
            created_at=self.database.from_db_datetime(row["created_at"])
            or datetime.now(UTC),
        )

    def _require_user(self, row: DBRow) -> User:
        user = self._row_to_user(row)
        if user is None:
            raise ValueError("Expected user row")
        return user
