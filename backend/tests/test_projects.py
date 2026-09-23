from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_create_project_requires_name():
    response = client.post(
        "/api/projects",
        json={
            "description": "Missing name",
        },
    )

    assert response.status_code == 422

def test_get_missing_project_returns_404():
    response = client.get("/api/projects/999999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"