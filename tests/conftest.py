import sqlite3
import pytest
import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    database_path = tmp_path / "test_urls.db"

    def get_test_db_connection():
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        return connection

    monkeypatch.setattr(
        app_module,
        "get_db_connection",
        get_test_db_connection
    )

    app_module.app.config.update(TESTING=True)

    app_module.init_db()

    with app_module.app.test_client() as test_client:
        yield test_client
        