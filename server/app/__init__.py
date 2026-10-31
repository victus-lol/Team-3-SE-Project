"""
Flask application factory and blueprint registration.
Owner: Akash Pawar (PES2UG24CS041) - application factory, blueprint wiring, CLI commands
Balaji Gowda S R (PES2UG25CS804) - auth, admin, dashboard blueprints
"""

import logging
import os

from flask import Flask, jsonify

from .common.responses import error_response, success_response
from .config import config_map
from .extensions import csrf, db, login_manager, migrate


def create_app(config_name: str | None = None) -> Flask:
    """
    Application factory.

    Args:
        config_name: One of 'development', 'testing', 'production'.
                     Falls back to FLASK_ENV env var, then 'development'.
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__, instance_relative_config=True)

    # ── Configuration ────────────────────────────────────────────────────────
    cfg = config_map.get(config_name)
    if cfg is None:
        raise ValueError(
            f"Unknown config '{config_name}'. Choose from: {list(config_map.keys())}"
        )
    app.config.from_object(cfg)
    cfg.init_app(app)

    # ── Ensure instance folder ───────────────────────────────────────────────
    os.makedirs(app.instance_path, exist_ok=True)

    # ── Extensions ───────────────────────────────────────────────────────────
    _init_extensions(app)

    if app.config.get("TESTING"):
        login_manager.session_protection = None

    # ── PRAGMA and engine events ─────────────────────────────────────────────
    _configure_sqlite(app)

    # ── Blueprints ───────────────────────────────────────────────────────────
    _register_blueprints(app)

    # ── Error handlers ───────────────────────────────────────────────────────
    _register_error_handlers(app)

    # ── CLI commands ─────────────────────────────────────────────────────────
    _register_cli(app)

    # ── Logging ──────────────────────────────────────────────────────────────
    if not app.debug and not app.testing:
        logging.basicConfig(level=logging.INFO)

    return app


def _init_extensions(app: Flask) -> None:
    """Initialize Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Import models so Alembic / migrate sees them
    with app.app_context():
        from .models import category, notification, task, user  # noqa: F401


def _configure_sqlite(app: Flask) -> None:
    """Enable FK enforcement and WAL on every SQLite connection."""
    import sqlalchemy.event as sa_event

    uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    is_memory = ":memory:" in uri or uri == "sqlite://"

    with app.app_context():
        engine = db.engine

        @sa_event.listens_for(engine, "connect", named=True)
        def set_sqlite_pragma(dbapi_connection, **kw):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute("PRAGMA busy_timeout=5000")
            if not is_memory:
                cursor.execute("PRAGMA journal_mode=WAL")
            cursor.close()


def _register_blueprints(app: Flask) -> None:
    """Register all feature blueprints."""
    from .admin.routes import admin_bp
    from .auth.routes import auth_bp
    from .categories.routes import categories_bp
    from .dashboard.routes import dashboard_bp
    from .notifications.routes import notifications_bp
    from .search.routes import search_bp
    from .tasks.routes import tasks_bp

    api_prefix = "/api"
    app.register_blueprint(auth_bp, url_prefix=f"{api_prefix}/auth")
    app.register_blueprint(tasks_bp, url_prefix=f"{api_prefix}/tasks")
    app.register_blueprint(categories_bp, url_prefix=f"{api_prefix}/categories")
    app.register_blueprint(search_bp, url_prefix=f"{api_prefix}")
    app.register_blueprint(dashboard_bp, url_prefix=f"{api_prefix}/dashboard")
    app.register_blueprint(notifications_bp, url_prefix=f"{api_prefix}/notifications")
    app.register_blueprint(admin_bp, url_prefix=f"{api_prefix}/admin")

    # ── Health / Readiness ────────────────────────────────────────────────────
    @app.route("/api/health", methods=["GET"])
    def health():
        """Health check — always returns 200 if the process is alive."""
        return jsonify({"status": "ok", "service": "task-manager-api"}), 200

    @app.route("/api/ready", methods=["GET"])
    def ready():
        """Readiness check — verifies DB connectivity."""
        try:
            from sqlalchemy import text as sql_text
            db.session.execute(sql_text("SELECT 1"))
            return jsonify(success_response({"db": "ok"}, "Service is ready")), 200
        except Exception:
            # Never expose internal details
            return (
                jsonify(
                    error_response("SERVICE_UNAVAILABLE", "Database not available")
                ),
                503,
            )


def _register_error_handlers(app: Flask) -> None:
    """Central JSON error responses."""
    from .middleware.error_handler import register_error_handlers
    register_error_handlers(app)


def _register_cli(app: Flask) -> None:
    """Register custom Flask CLI commands."""
    import click

    from .auth.service import create_admin_user

    @app.cli.command("create-admin")
    @click.option("--name", prompt="Admin name", help="Full name of the admin user")
    @click.option("--email", prompt="Admin email", help="Email address")
    @click.option(
        "--password",
        prompt=True,
        hide_input=True,
        confirmation_prompt=True,
        help="Password",
    )
    def create_admin_cmd(name: str, email: str, password: str):
        """Create the initial administrator account."""
        try:
            user = create_admin_user(name=name, email=email, password=password)
            click.echo(f"Admin created: {user.email} (id={user.id})")
        except Exception as exc:
            click.echo(f"Error: {exc}", err=True)
            raise SystemExit(1)

    app.cli.add_command(create_admin_cmd)

