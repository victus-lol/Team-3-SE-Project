"""
Categories API integration tests.
Owner: Aadi Kore (PES2UG24CS006)
Sprint: S2 (S2-01)
"""


class TestCategoriesApiLive:
    def test_list_categories_unauthenticated_returns_401(self, client):
        response = client.get("/api/categories")
        assert response.status_code == 401


class TestCategoriesApi:
    def test_list_categories_authenticated(self, auth_client, sample_category):
        response = auth_client.get("/api/categories")

        assert response.status_code == 200

        data = response.get_json()
        assert data["success"] is True
        assert any(category["id"] == sample_category.id for category in data["data"])

    def test_category_not_visible_to_other_user(self, auth_client, db, test_admin):
        from app.models.category import Category

        category = Category.create(test_admin.id, "private")
        db.session.add(category)
        db.session.commit()

        response = auth_client.get("/api/categories")

        assert response.status_code == 200

        data = response.get_json()
        assert all(item["user_id"] != test_admin.id for item in data["data"])

    def test_create_category_normalizes_name(self, auth_client):
        response = auth_client.post("/api/categories", json={"name": "  Research  "})

        assert response.status_code == 201
        assert response.get_json()["data"]["name"] == "research"

    def test_create_duplicate_category_returns_conflict(self, auth_client, sample_category):
        response = auth_client.post("/api/categories", json={"name": sample_category.name.upper()})

        assert response.status_code == 409

    def test_create_category_validates_name(self, auth_client):
        response = auth_client.post("/api/categories", json={"name": " "})

        assert response.status_code == 400
