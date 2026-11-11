"""
Flask extensions — single instances shared across the application.
Owner: Akash Pawar (PES2UG24CS041), coordinated with Balaji Gowda S R (PES2UG25CS804)
"""

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# SQLAlchemy instance — imported by models, services and tests
db = SQLAlchemy()

# Alembic-backed migration tool
migrate = Migrate()

# Session / identity management
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # endpoint name for @login_required redirect
login_manager.login_message_category = "info"
login_manager.session_protection = "strong"

# CSRF protection
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id: str):
    """Load user from DB for Flask-Login."""
    from .models.user import User

    return User.query.get(int(user_id))
