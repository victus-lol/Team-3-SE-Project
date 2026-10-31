"""
Centralized application configuration.
Owner: Balaji Gowda S R (PES2UG25CS804)

Three environments:
  development  – local development, debug on, SQLite file
  testing      – automated tests, in-memory SQLite, CSRF disabled
  production   – hardened, requires SECRET_KEY env var

Reading env vars: use os.environ.get() with safe defaults. Never hard-code secrets.
Production fails fast if SECRET_KEY is missing.
"""

import os
from pathlib import Path

# Resolve the project root (three levels up from this file: app/ → server/ → task-manager/)
_HERE = Path(__file__).resolve().parent          # server/app/
_SERVER_DIR = _HERE.parent                       # server/
_PROJECT_ROOT = _SERVER_DIR.parent               # task-manager/
_INSTANCE_DIR = _PROJECT_ROOT / "instance"


class BaseConfig:
    """Shared settings inherited by all environments."""

    # ── Security ──────────────────────────────────────────────────────────────
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    WTF_CSRF_ENABLED: bool = True
    WTF_CSRF_TIME_LIMIT: int = 3600  # seconds

    # Session cookie settings (hardened for production — see ProductionConfig)
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "Lax"
    SESSION_COOKIE_SECURE: bool = False  # overridden in production
    REMEMBER_COOKIE_HTTPONLY: bool = True
    REMEMBER_COOKIE_SAMESITE: str = "Lax"
    PERMANENT_SESSION_LIFETIME: int = 86400  # 24 hours

    # ── Database ──────────────────────────────────────────────────────────────
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False

    # ── Application ───────────────────────────────────────────────────────────
    JSON_SORT_KEYS: bool = False
    APP_TIMEZONE: str = os.environ.get("APP_TIMEZONE", "UTC")

    @classmethod
    def init_app(cls, app):
        """Called by the factory after from_object()."""
        pass


class DevelopmentConfig(BaseConfig):
    """Development environment — debug on, file-based SQLite."""

    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{_INSTANCE_DIR / 'task_manager.sqlite'}",
    )
    SQLALCHEMY_ECHO: bool = bool(os.environ.get("SQLALCHEMY_ECHO", ""))

    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        # Ensure instance dir exists
        _INSTANCE_DIR.mkdir(parents=True, exist_ok=True)


class TestingConfig(BaseConfig):
    """
    Testing environment — isolated in-memory SQLite.

    CRITICAL: This config MUST NOT reference the developer's database.
    Tests assert this via the test_db_isolation test in test_health_api.py.
    """

    TESTING: bool = True
    DEBUG: bool = False

    # Use an isolated temporary file-based DB (created per-session in conftest.py)
    # so FK enforcement works; conftest overrides this to a tmp path.
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"

    # Disable CSRF for the automated test client
    WTF_CSRF_ENABLED: bool = False
    WTF_CSRF_METHODS: list = []

    # Faster password hashing in tests
    BCRYPT_LOG_ROUNDS: int = 4

    SERVER_NAME: str = "localhost"

    @classmethod
    def init_app(cls, app):
        super().init_app(app)


class ProductionConfig(BaseConfig):
    """
    Production environment.
    Fails fast if SECRET_KEY is not set to a non-default value.
    """

    DEBUG: bool = False
    SESSION_COOKIE_SECURE: bool = True
    REMEMBER_COOKIE_SECURE: bool = True
    WTF_CSRF_SSL_STRICT: bool = True

    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{_INSTANCE_DIR / 'task_manager.sqlite'}",
    )

    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        # Fail fast on missing or default secret key
        secret = app.config.get("SECRET_KEY", "")
        if not secret or secret == "dev-secret-change-in-production":
            raise RuntimeError(
                "SECRET_KEY environment variable must be set to a strong random value "
                "in production. Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
            )
        # Ensure instance dir exists
        _INSTANCE_DIR.mkdir(parents=True, exist_ok=True)


config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    # Default alias
    "default": DevelopmentConfig,
}

