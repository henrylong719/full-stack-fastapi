import os
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.core.config import settings
from app.models import ItemCreate, UserCreate


def seed_mock_data() -> None:
    if settings.ENVIRONMENT != "local":
        return

    if not settings.MYSQL_SEED_LOCAL_DATA:
        return

    from app.crud.items import create_item
    from app.crud.users import create_user, list_all_users

    if list_all_users():
        return

    admin = create_user(
        user_create=UserCreate(
            email="admin@example.com",
            full_name="Admin User",
            is_active=True,
            is_superuser=True,
            password=os.getenv("SEED_ADMIN_PASSWORD", "changethis123"),
        )
    )
    alice = create_user(
        user_create=UserCreate(
            email="alice@example.com",
            full_name="Alice",
            is_active=True,
            is_superuser=False,
            password=os.getenv("SEED_USER_PASSWORD", "password123"),
        )
    )

    create_item(
        item_in=ItemCreate(
            title="Camping Tent",
            description="2-person tent, lightweight",
        ),
        owner_id=alice.id,
    )
    create_item(
        item_in=ItemCreate(
            title="Portable Stove",
            description="Small gas camping stove",
        ),
        owner_id=alice.id,
    )
    create_item(
        item_in=ItemCreate(
            title="Admin Test Item",
            description="Seed item owned by admin",
        ),
        owner_id=admin.id,
    )


def main() -> None:
    from app.repositories import initialize_repositories

    try:
        initialize_repositories()
        seed_mock_data()
    except Exception as exc:
        print(f"Seed failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print("Seed completed successfully.")


if __name__ == "__main__":
    main()
