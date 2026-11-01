"""
Reset test data script.
Owner: Akash Pawar (PES2UG24CS041)

Refuses to run in production.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "server")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.task import Task
from app.models.category import Category
from app.models.notification import Notification

def reset():
    env = os.environ.get("FLASK_ENV", "development")
    if env == "production":
        print("ERROR: Cannot reset database in production environment!", file=sys.stderr)
        sys.exit(1)

    app = create_app(env)
    with app.app_context():
        print(f"Clearing tables in '{env}'...")
        db.session.execute(Notification.__table__.delete())
        db.session.execute(Task.__table__.delete())
        db.session.execute(Category.__table__.delete())
        db.session.execute(User.__table__.delete())
        db.session.commit()
        print("Reset complete.")

if __name__ == "__main__":
    reset()

