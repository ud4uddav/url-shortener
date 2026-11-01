
import sqlite3
import secrets
import string

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    abort,
    url_for
)

from urllib.parse import urlparse

app = Flask(__name__)


# 1. Database connection
def get_db_connection():
    connection = sqlite3.connect("urls.db")
    connection.row_factory = sqlite3.Row
    return connection


# 2. Initialize database
def init_db():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE,
            clicks INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


# 3. Generate short code
def generate_short_code():

    characters = string.ascii_letters + string.digits

    return ''.join(
        secrets.choice(characters)
        for _ in range(6)
    )


# 4. Validate URL
def is_valid_url(url):

    parsed_url = urlparse(url)

    return (
        parsed_url.scheme in ["http", "https"]
        and bool(parsed_url.netloc)
    )


# 5. Homepage
@app.route("/")
def home():
    return render_template("index.html")


# 6. Shorten URL
@app.route("/shorten", methods=["POST"])
def shorten():

    original_url = request.form.get(
        "original_url", ""
    ).strip()

    if not is_valid_url(original_url):
        return render_template(
            "index.html",
            error="Please enter a valid HTTP or HTTPS URL."
        )

    connection = get_db_connection()
    short_code = None

    for attempt in range(5):

        candidate = generate_short_code()

        try:
            connection.execute(
                """
                INSERT INTO urls (original_url, short_code)
                VALUES (?, ?)
                """,
                (original_url, candidate)
            )

            connection.commit()
            short_code = candidate
            break

        except sqlite3.IntegrityError:
            continue

    connection.close()

    if short_code is None:
        return "Could not generate a unique code.", 500

    short_url = url_for(
        "redirect_url",
        short_code=short_code,
        _external=True
    )

    return render_template(
        "index.html",
        short_url=short_url
    )


# 7. Redirect to original URL
@app.route("/<short_code>")
def redirect_url(short_code):

    connection = get_db_connection()

    url_data = connection.execute(
        "SELECT original_url FROM urls WHERE short_code = ?",
        (short_code,)
    ).fetchone()

    if url_data is None:
        connection.close()
        abort(404)

    connection.execute(
        "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
        (short_code,)
    )

    connection.commit()
    connection.close()

    return redirect(url_data["original_url"])


# 8. Statistics page
@app.route("/stats")
def stats():

    connection = get_db_connection()

    urls = connection.execute(
        "SELECT * FROM urls ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "stats.html",
        urls=urls
    )


# 9. Start application
if __name__ == "__main__":

    init_db()

    app.run(debug=True)
