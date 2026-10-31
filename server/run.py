"""
Flask application entry point.
Run with: flask run   (after setting FLASK_APP=run.py)
Or:        python run.py
"""

import os

from app import create_app

app = create_app(os.environ.get("FLASK_ENV", "development"))

if __name__ == "__main__":
    app.run(
        host=os.environ.get("FLASK_HOST", "127.0.0.1"),
        port=int(os.environ.get("FLASK_PORT", 5000)),
        debug=app.config.get("DEBUG", False),
    )

