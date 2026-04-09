MYSQL_SCHEMA_STATEMENTS = (
    """
    CREATE TABLE IF NOT EXISTS users (
        id CHAR(36) PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        full_name VARCHAR(255) NULL,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
        hashed_password VARCHAR(255) NOT NULL,
        created_at DATETIME(6) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    """
    CREATE TABLE IF NOT EXISTS items (
        id CHAR(36) PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT NULL,
        owner_id CHAR(36) NOT NULL,
        created_at DATETIME(6) NOT NULL,
        CONSTRAINT fk_items_owner
            FOREIGN KEY (owner_id) REFERENCES users(id)
            ON DELETE CASCADE,
        INDEX idx_items_owner_created_at (owner_id, created_at),
        INDEX idx_items_created_at (created_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
)
