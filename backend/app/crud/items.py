from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.models import Item, ItemCreate, ItemUpdate
from app.repositories import get_item_repository


def create_item(*, item_in: ItemCreate, owner_id: UUID) -> Item:
    item = Item(
        id=uuid4(),
        title=item_in.title,
        description=item_in.description,
        owner_id=owner_id,
        created_at=datetime.now(UTC),
    )
    return get_item_repository().create(item)


def get_item(*, item_id: UUID) -> Item | None:
    return get_item_repository().get(item_id)


def get_items(*, skip: int = 0, limit: int = 100) -> tuple[list[Item], int]:
    return get_item_repository().list(skip=skip, limit=limit)


def get_items_by_owner(
    *, owner_id: UUID, skip: int = 0, limit: int = 100
) -> tuple[list[Item], int]:
    return get_item_repository().list_by_owner(
        owner_id=owner_id,
        skip=skip,
        limit=limit,
    )


def update_item(*, item: Item, item_in: ItemUpdate) -> Item:
    update_data = item_in.model_dump(exclude_unset=True)

    if "title" in update_data and update_data["title"] is not None:
        item.title = update_data["title"]
    if "description" in update_data:
        item.description = update_data["description"]

    return get_item_repository().update(item)


def delete_item(*, item: Item) -> None:
    get_item_repository().delete(item_id=item.id)


def delete_items_by_owner(*, owner_id: UUID) -> int:
    return get_item_repository().delete_by_owner(owner_id=owner_id)


def list_all_items() -> list[Item]:
    return get_item_repository().list_all()
