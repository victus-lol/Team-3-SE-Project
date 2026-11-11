class TestTasksApiLive:

    def test_list_tasks_unauthenticated_returns_401(self, client):
        assert client.get("/api/tasks").status_code == 401

    def test_create_task_unauthenticated_returns_401(self, client):
        response = client.post("/api/tasks", json={"title": "Test"})
        assert response.status_code == 401

    def test_get_task_unauthenticated_returns_401(self, client):
        assert client.get("/api/tasks/1").status_code == 401


class TestTasksCrud:

    def test_create_task_authenticated(self, auth_client):
        response = auth_client.post(
            "/api/tasks",
            json={"title": "New task"},
        )
        assert response.status_code == 201

    def test_list_tasks_returns_only_owned(
        self, auth_client, test_user, test_admin, db
    ):
        from app.models.task import Task

        db.session.add(Task(owner_id=test_user.id, title="Mine"))
        db.session.add(Task(owner_id=test_admin.id, title="Theirs"))
        db.session.commit()

        response = auth_client.get("/api/tasks")
        assert response.status_code == 200

        tasks = response.get_json()["data"]
        assert all(task["owner_id"] == test_user.id for task in tasks)

    def test_update_own_task(self, auth_client, sample_task):
        response = auth_client.patch(
            f"/api/tasks/{sample_task.id}",
            json={"title": "Updated"},
        )
        assert response.status_code == 200

    def test_update_another_users_task_returns_404(
        self, auth_client, db, test_admin
    ):
        from app.models.task import Task

        task = Task(owner_id=test_admin.id, title="Private")
        db.session.add(task)
        db.session.commit()

        response = auth_client.patch(
            f"/api/tasks/{task.id}",
            json={"title": "Changed"},
        )
        assert response.status_code == 404

    def test_delete_own_task(self, auth_client, sample_task):
        response = auth_client.delete(
            f"/api/tasks/{sample_task.id}"
        )
        assert response.status_code == 200