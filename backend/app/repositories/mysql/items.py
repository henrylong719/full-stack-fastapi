from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from app.db.mysql import DBRow, MySQLDatabase
from app.models import Item


class MySQLItemRepository:
    def __init__(self, database: MySQLDatabase) -> None:
        self.database = database

    def get(self, item_id: UUID) -> Item | None:
        row = self.database.fetch_one(
            """
            SELECT id, title, description, owner_id, created_at
            FROM items
            WHERE id = %s
            LIMIT 1
            """,
            (str(item_id),),
        )
        return self._row_to_item(row)

    def list(self, *, skip: int = 0, limit: int = 100) -> tuple[list[Item], int]:
        rows = self.database.fetch_all(
            """
            SELECT id, title, description, owner_id, created_at
            FROM items
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, skip),
        )
        count_row = self.database.fetch_one("SELECT COUNT(*) AS count FROM items")
        count = int(count_row["count"]) if count_row else 0
        return [self._require_item(row) for row in rows], count

    def list_by_owner(
        self, *, owner_id: UUID, skip: int = 0, limit: int = 100
    ) -> tuple[list[Item], int]:
        rows = self.database.fetch_all(
            """
            SELECT id, title, description, owner_id, created_at
            FROM items
            WHERE owner_id = %s
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
            """,
            (str(owner_id), limit, skip),
        )
        count_row = self.database.fetch_one(
            "SELECT COUNT(*) AS count FROM items WHERE owner_id = %s",
            (str(owner_id),),
        )
        count = int(count_row["count"]) if count_row else 0
        return [self._require_item(row) for row in rows], count

    def create(self, item: Item) -> Item:
        self.database.execute(
            """
            INSERT INTO items (id, title, description, owner_id, created_at)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                str(item.id),
                item.title,
                item.description,
                str(item.owner_id),
                self.database.to_db_datetime(item.created_at),
            ),
        )
        return item

    def update(self, item: Item) -> Item:
        self.database.execute(
            """
            UPDATE items
            SET title = %s,
                description = %s
            WHERE id = %s
            """,
            (item.title, item.description, str(item.id)),
        )
        return item

    def delete(self, *, item_id: UUID) -> None:
        self.database.execute("DELETE FROM items WHERE id = %s", (str(item_id),))

    def delete_by_owner(self, *, owner_id: UUID) -> int:
        return self.database.execute(
            "DELETE FROM items WHERE owner_id = %s",
            (str(owner_id),),
        )

    def list_all(self) -> list[Item]:
        rows = self.database.fetch_all(
            """
            SELECT id, title, description, owner_id, created_at
            FROM items
            ORDER BY created_at DESC
            """
        )
        return [self._require_item(row) for row in rows]

    def _row_to_item(self, row: DBRow | None) -> Item | None:
        if not row:
            return None

        return Item(
            id=UUID(row["id"]),
            title=row["title"],
            description=row["description"],
            owner_id=UUID(row["owner_id"]),
            created_at=self.database.from_db_datetime(row["created_at"])
            or datetime.now(UTC),
        )

    def _require_item(self, row: DBRow) -> Item:
        item = self._row_to_item(row)
        if item is None:
            raise ValueError("Expected item row")
        return item
