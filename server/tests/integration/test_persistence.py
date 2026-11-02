"""
Persistence integration tests — data must survive DB session close/reopen.
Owner: Aadi Kore (PES2UG24CS006) + Akash Pawar (PES2UG24CS041)
Sprint: S2 (S2-10)
Requirement IDs: TMA-NF-001
"""

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from app.extensions import db
from app.models.task import Task
from app.models.user import User


class TestPersistence:
    def test_task_persists_after_db_session_close(self, tmp_path):
        """
        TC-Data-01 | Owner: Aadi+Akash | Requirement: TMA-NF-001 | Backlog: S2-10

        A task committed to an isolated file-backed SQLite database remains
        readable after the first SQLAlchemy session is closed and a new
        independent session/connection is opened.

        The database file is created under pytest's per-test tmp_path. This
        test does not depend on or touch the developer's normal database.
        """
        database_file = tmp_path / "persistence_regression.sqlite"
        engine = create_engine(URL.create("sqlite", database=str(database_file)))
        session_factory = sessionmaker(bind=engine)

        try:
            db.metadata.create_all(bind=engine)

            with session_factory() as first_session:
                user = User.create(
                    name="Persistence Test User",
                    email="persistence-test@example.com",
                    password="password123",
                )
                first_session.add(user)
                first_session.flush()

                task = Task(
                    owner_id=user.id,
                    title="Persistence regression task",
                    description="Must survive closing and reopening the DB session.",
                    priority="high",
                    status="pending",
                )
                first_session.add(task)
                first_session.commit()

                task_id = task.id
                owner_id = user.id

            # The context manager above has closed the first session. Create
            # a fresh session, which reads from the same on-disk SQLite file.
            with session_factory() as reopened_session:
                persisted_task = reopened_session.get(Task, task_id)

                assert persisted_task is not None
                assert persisted_task.id == task_id
                assert persisted_task.owner_id == owner_id
                assert persisted_task.title == "Persistence regression task"
                assert persisted_task.description == (
                    "Must survive closing and reopening the DB session."
                )
                assert persisted_task.priority == "high"
                assert persisted_task.status == "pending"
        finally:
            engine.dispose()
