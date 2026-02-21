from uuid import UUID

from app.models import Item, ItemCreate, ItemUpdate

_ITEMS_BY_ID: dict[UUID, Item] = {}


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


def delete_items_by_owner(*, owner_id: UUID) -> int:
    to_delete = [
        item_id for item_id, item in _ITEMS_BY_ID.items() if item.owner_id == owner_id
    ]
    for item_id in to_delete:
        _ITEMS_BY_ID.pop(item_id, None)
    return len(to_delete)


def list_all_items() -> list[Item]:
    return list(_ITEMS_BY_ID.values())
