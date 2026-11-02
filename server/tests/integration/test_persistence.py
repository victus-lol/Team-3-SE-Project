"""
Persistence integration tests — data must survive session close/reopen.
Owner: Aadi Kore (PES2UG24CS006) + Akash Pawar (PES2UG24CS041)
Sprint: S2 (S2-10)
Requirement IDs: TMA-NF-001
"""

from app.models.task import Task


class TestPersistence:
    def test_task_persists_after_db_session_close(self, db, test_user):
        """
        TC-Data-01 | Owner: Aadi+Akash | Requirement: TMA-NF-001 | Backlog: S2-10

        A task committed to the isolated file-backed SQLite test DB remains
        readable after the scoped SQLAlchemy session is removed and the engine
        connection pool is disposed. The next read must open a fresh connection
        to the same SQLite file.

        The shared test fixture points at its own temporary database; this test
        never uses the developer's normal database.
        """
        owner_id = test_user.id
        task = Task(
            owner_id=owner_id,
            title="Persistence regression task",
            description="Must remain available after closing and reopening the DB session.",
            priority="high",
            status="pending",
        )
        db.session.add(task)
        db.session.commit()
        task_id = task.id

        database_path = db.engine.url.database
        assert database_path and database_path != ":memory:"

        # Close the current scoped session and force the next query to obtain a
        # new DBAPI connection instead of reusing a connection from the pool.
        db.session.remove()
        db.engine.dispose()

        persisted_task = db.session.get(Task, task_id)

        assert persisted_task is not None
        assert persisted_task.id == task_id
        assert persisted_task.owner_id == owner_id
        assert persisted_task.title == "Persistence regression task"
        assert persisted_task.description == (
            "Must remain available after closing and reopening the DB session."
        )
        assert persisted_task.priority == "high"
        assert persisted_task.status == "pending"
