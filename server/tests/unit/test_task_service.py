import pytest

from app.common.exceptions import NotFoundError, ValidationError
from app.models.category import Category
from app.models.task import Task
from app.tasks.service import (
    create_task,
    delete_task,
    get_task_or_404,
    list_tasks,
    update_task,
)


class TestTaskService:
    def test_create_task_valid(self, db, test_user):
        task = create_task(
            test_user.id,
            {
                "title": "Finish project",
                "description": "Complete backend",
                "priority": "high",
            },
        )

        assert task.id is not None
        assert task.owner_id == test_user.id
        assert task.title == "Finish project"

    def test_create_task_empty_title_rejected(self, db, test_user):
        with pytest.raises(ValidationError):
            create_task(test_user.id, {"title": ""})

    def test_list_tasks_scoped_to_owner(self, db, test_user, test_admin):
        create_task(test_user.id, {"title": "User task"})
        create_task(test_admin.id, {"title": "Admin task"})

        tasks = list_tasks(test_user.id)

        assert len(tasks) == 1
        assert tasks[0].title == "User task"

    def test_get_task_other_user_returns_404(self, db, test_user, test_admin, sample_task):
        with pytest.raises(NotFoundError):
            get_task_or_404(sample_task.id, test_admin.id)

    def test_update_task_owned(self, db, test_user, sample_task):
        updated = update_task(
            sample_task.id,
            test_user.id,
            {"title": "Updated task", "priority": "high"},
        )

        assert updated.title == "Updated task"
        assert updated.priority == "high"

    def test_delete_task_owned(self, db, test_user, sample_task):
        task_id = sample_task.id

        delete_task(task_id, test_user.id)

        assert db.session.get(Task, task_id) is None

    def test_category_cross_user_rejected(self, db, test_user, test_admin):
        category = Category.create(test_admin.id, "private")
        db.session.add(category)
        db.session.commit()

        with pytest.raises(NotFoundError):
            create_task(
                test_user.id,
                {
                    "title": "Invalid category task",
                    "category_id": category.id,
                },
            )
