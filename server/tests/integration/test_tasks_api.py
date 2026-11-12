class TestTasksApiLive:
    def test_list_tasks_unauthenticated_returns_401(self, client):
        assert client.get("/api/tasks").status_code == 401

    def test_create_task_unauthenticated_returns_401(self, client):
        response = client.post("/api/tasks", json={"title": "Test"})
        assert response.status_code == 401

    def test_get_task_unauthenticated_returns_401(self, client):
        assert client.get("/api/tasks/1").status_code == 401

    def test_task_list_includes_pagination_metadata(self, auth_client, db, test_user):
        from app.models.task import Task

        db.session.add_all(
            [Task(owner_id=test_user.id, title=f"Page task {index}") for index in range(3)]
        )
        db.session.commit()

        first = auth_client.get("/api/tasks?page=1&per_page=2").get_json()
        final = auth_client.get("/api/tasks?page=2&per_page=2").get_json()

        assert len(first["data"]) == 2
        assert first["pagination"] == {
            "page": 1,
            "per_page": 2,
            "total_items": 3,
            "total_pages": 2,
            "has_next": True,
            "has_previous": False,
        }
        assert len(final["data"]) == 1
        assert final["pagination"]["has_previous"] is True

    def test_task_list_rejects_invalid_page_values(self, auth_client):
        for query in ("page=0", "page=abc", "per_page=101"):
            assert auth_client.get(f"/api/tasks?{query}").status_code == 400

    def test_task_list_pagination_remains_user_scoped(self, auth_client, db, test_user, test_admin):
        from app.models.task import Task

        db.session.add_all(
            [
                Task(owner_id=test_user.id, title="Visible"),
                Task(owner_id=test_admin.id, title="Private"),
            ]
        )
        db.session.commit()

        response = auth_client.get("/api/tasks?page=1&per_page=10")

        assert [task["title"] for task in response.get_json()["data"]] == ["Visible"]
        assert response.get_json()["pagination"]["total_items"] == 1


class TestTasksCrud:
    def test_create_task_authenticated(self, auth_client):
        response = auth_client.post(
            "/api/tasks",
            json={"title": "New task"},
        )
        assert response.status_code == 201

    def test_list_tasks_returns_only_owned(self, auth_client, test_user, test_admin, db):
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

    def test_update_another_users_task_returns_404(self, auth_client, db, test_admin):
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
        response = auth_client.delete(f"/api/tasks/{sample_task.id}")
        assert response.status_code == 200
