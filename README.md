# URL Shortener

A lightweight URL shortener built with **Python**, **Flask**, and **SQLite**. Enter a web address to create a compact link, then use the link to redirect visitors to the original page.

[![Live demo](https://img.shields.io/badge/Live%20demo-Open%20app-5b5ce2?style=for-the-badge)](https://url-shortener-mix4.onrender.com/)
[![CI](https://github.com/ud4uddav/url-shortener/actions/workflows/ci.yml/badge.svg)](https://github.com/ud4uddav/url-shortener/actions/workflows/ci.yml)

## Try it

- **Application:** [url-shortener-mix4.onrender.com](https://url-shortener-mix4.onrender.com/)
- **Saved URLs and click counts:** [View statistics](https://url-shortener-mix4.onrender.com/stats)

Paste a URL beginning with `http://` or `https://` into the form and select **Shorten URL**. The app creates a six-character code and returns a link on its own domain. Opening that link looks up the code and redirects to the original URL.

## Features

- Generates random six-character short codes
- Validates HTTP and HTTPS URLs
- Redirects short links to their original destinations
- Tracks clicks for each short link
- Displays saved links and click counts on a statistics page
- Creates the SQLite table automatically when the app starts

## How it works

1. The Flask route validates the submitted URL.
2. The app generates a short code and stores the original URL and code in SQLite.
3. Visiting `/<short_code>` looks up the original URL, increments its click count, and redirects the visitor.
4. The `/stats` page lists the saved URL records and click counts.

## Run locally

### Requirements

- Python 3.12 or newer
- pip

### Setup

```bash
git clone https://github.com/ud4uddav/url-shortener.git
cd url-shortener
python -m venv .venv
```

Activate the environment:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies and start the development server:

```bash
python -m pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000/) in your browser. The SQLite file (`urls.db`) is created in the application directory when the app starts.

## Run with Docker

```bash
docker build -t url-shortener .
docker run --rm -p 5000:5000 url-shortener
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000/).

## Tests and continuous integration

Run the test suite locally:

```bash
python -m pytest -v
```

GitHub Actions runs the tests and builds the Docker image on pushes and pull requests targeting `main`. See the [CI workflow](.github/workflows/ci.yml).

## Technology

- **Backend:** Python, Flask, Gunicorn
- **Database:** SQLite
- **Frontend:** HTML, CSS, Jinja2 templates
- **Containerization:** Docker
- **CI:** GitHub Actions
- **Hosting:** Render

## Storage note

This project uses a local SQLite database. On Render's free service, local files are ephemeral, so saved links may be lost when the service restarts or is redeployed. The live demo is intended for demonstration; it does not use persistent database storage.
