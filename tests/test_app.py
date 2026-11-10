import app as app_module


def test_database_connection():
    connection = app_module.get_db_connection()

    assert connection is not None

    connection.close()

def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200

def test_urls_table_exists(client):
    connection = app_module.get_db_connection()

    cursor = connection.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = 'urls'
    """)

    table = cursor.fetchone()

    connection.close()

    assert table is not None
    assert table["name"] == "urls"

def test_shorten_valid_url(client):
    response = client.post(
        "/shorten",
        data={
            "original_url": "https://example.com"
        }
    )

    assert response.status_code == 200   

def test_missing_url_is_not_saved(client):
    response = client.post(
        "/shorten",
        data={}
    )

    assert response.status_code == 200
def test_redirect_to_original_url(client):
    connection = app_module.get_db_connection()

    connection.execute(
        """
        INSERT INTO urls (original_url, short_code)
        VALUES (?, ?)
        """,
        ("https://example.com", "abc123")
    )

    connection.commit()
    connection.close()

    response = client.get(
        "/abc123",
        follow_redirects=False
    )

    assert response.status_code == 302
    assert response.location == "https://example.com"

def test_unknown_short_code(client):
    response = client.get("/unknown")

    assert response.status_code == 404

def test_stats_page(client):
    response = client.get("/stats")

    assert response.status_code == 200

def test_stats_page_displays_saved_url(client):
    connection = app_module.get_db_connection()

    connection.execute(
        """
        INSERT INTO urls (original_url, short_code)
        VALUES (?, ?)
        """,
        ("https://example.com", "abc123")
    )

    connection.commit()
    connection.close()

    response = client.get("/stats")

    assert response.status_code == 200
    assert b"https://example.com" in response.data
    

