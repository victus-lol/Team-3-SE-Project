"""
Seed script for development environments.
Owner: Akash Pawar (PES2UG24CS041)

Refuses to run in production.
"""

import os
import sys

# Ensure server module is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "server")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.category import Category
from app.models.task import Task

def seed():
    env = os.environ.get("FLASK_ENV", "development")
    if env == "production":
        print("ERROR: Cannot seed database in production environment!", file=sys.stderr)
        sys.exit(1)

    app = create_app(env)
    with app.app_context():
        print(f"Seeding database for '{env}'...")
        # Check if users already exist
        if User.query.filter_by(email="demo@example.com").first():
            print("Database already contains seed data.")
            return

        demo_user = User.create(name="Demo User", email="demo@example.com", password="password123", role="user")
        admin_user = User.create(name="Admin User", email="admin@example.com", password="adminpassword123", role="admin")
        db.session.add_all([demo_user, admin_user])
        db.session.commit()

        cat_work = Category.create(user_id=demo_user.id, name="work")
        cat_personal = Category.create(user_id=demo_user.id, name="personal")
        db.session.add_all([cat_work, cat_personal])
        db.session.commit()

        task1 = Task(owner_id=demo_user.id, title="Complete Sprint 1 deliverables", description="Implement foundation and skeletons", priority="high", status="in_progress", category_id=cat_work.id)
        task2 = Task(owner_id=demo_user.id, title="Buy groceries", description="Milk, bread, eggs", priority="low", status="pending", category_id=cat_personal.id)
        db.session.add_all([task1, task2])
        db.session.commit()

        print("Seeding complete successfully.")

if __name__ == "__main__":
    seed()

