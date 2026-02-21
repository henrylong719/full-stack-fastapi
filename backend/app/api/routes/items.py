# backend/app/api/routes/items.py
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException, Path, Query, status

from app import crud
from app.api.deps import CurrentUser
from app.models import (
    ItemCreate,
    ItemPublic,
    ItemsPublic,
    ItemUpdate,
    Message,
)

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/")
def read_items(
    current_user: CurrentUser,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> ItemsPublic:
    if current_user.is_superuser:
        items, count = crud.get_items(skip=skip, limit=limit)
    else:
        items, count = crud.get_items_by_owner(owner_id=current_user.id, skip=skip, limit=limit)

    return ItemsPublic(
        data=[ItemPublic.model_validate(item) for item in items],
        count=count,
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item(
    current_user: CurrentUser,
    item_in: Annotated[ItemCreate, Body()],
) -> ItemPublic:
    item = crud.create_item(item_in=item_in, owner_id=current_user.id)
    return ItemPublic.model_validate(item)


@router.get("/{item_id}")
def read_item(
    current_user: CurrentUser,
    item_id: Annotated[UUID, Path()],
) -> ItemPublic:
    item = crud.get_item(item_id=item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    if not current_user.is_superuser and item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return ItemPublic.model_validate(item)


@router.patch("/{item_id}")
def update_item(
    current_user: CurrentUser,
    item_id: Annotated[UUID, Path()],
    item_in: Annotated[ItemUpdate, Body()],
) -> ItemPublic:
    item = crud.get_item(item_id=item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    if not current_user.is_superuser and item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    item = crud.update_item(item=item, item_in=item_in)
    return ItemPublic.model_validate(item)


@router.delete("/{item_id}")
def delete_item(
    current_user: CurrentUser,
    item_id: Annotated[UUID, Path()],
) -> Message:
    item = crud.get_item(item_id=item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    if not current_user.is_superuser and item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    crud.delete_item(item=item)
    return Message(message="Item deleted successfully")