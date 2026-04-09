import os

import pytest
from fastapi.testclient import TestClient
from mysql.connector import Error as MySQLError

os.environ["MYSQL_DATABASE"] = os.getenv(
    "MYSQL_TEST_DATABASE",
    "full_stack_fastapi_test",
)
os.environ["MYSQL_AUTO_CREATE_DATABASE"] = "true"
os.environ["MYSQL_AUTO_CREATE_TABLES"] = "true"
os.environ["MYSQL_SEED_LOCAL_DATA"] = "true"

from app import crud
from app.main import app


@pytest.fixture(autouse=True)
def reset_data_store():
    """
    Reset MySQL-backed test state before each test.
    """
    try:
        crud.reset_data_store()
    except MySQLError as exc:
        pytest.skip(f"MySQL is unavailable for backend tests: {exc}")
    yield
    try:
        crud.reset_data_store()
    except MySQLError:
        pass


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
