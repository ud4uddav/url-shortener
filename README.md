
# URL Shortener

A URL Shortener application built using Python and Flask.

## Features

- Convert long URLs into short URLs
- Generate random short codes
- Redirect users to original URLs
- SQLite database integration
- URL validation
- Click tracking
- URL statistics dashboard

## Technologies

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja2
- Git and GitHub

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd url-shortener
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it on macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

Test type	What it tests	URL Shortener example
Unit test	One small function	Generate a six-character code
Integration test	Multiple components working together	Flask route + SQLite
Functional test	Application feature	Submit URL and get short URL
End-to-end test	Complete user journey	Open website, submit URL, follow redirect

For this project:
- Testing a function that generates a short code is a unit test.
- Testing a Flask route that saves to SQLite is an integration test.
- Testing the complete shortening feature is a functional test.

