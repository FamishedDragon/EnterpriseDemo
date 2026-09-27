from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_create_work_item_valid():
    response = client.post(
        "/api/work-items",
        json={
            "project_id": 1,
            "title": "build dashboard",
            "priority": "high"
        },
    )

    assert response.status_code == 201

def test_create_pwork_item_invalid_priority():
    response = client.post(
        "/api/work-items",
        json={
            "title": "broken test",
            "priority": "invalid priority"
        },
    )

    assert response.status_code == 422

def test_create_work_item_requires_project():
    response = client.post(
        "/api/work-items",
        json={
            "project_id": 999999999,
            "title": "project not found test",
            "priority": "low"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"

def test_create_work_item_requires_title():
    response = client.post(
        "/api/work-items",
        json={
            "project_id": 1,
            "priority": "low"
        },
    )

    assert response.status_code == 422

def test_create_work_item():
    # Create a project first so we have a valid project_id.
    project_response = client.post(
        "/api/projects",
        json={
            "name": "Test Project",
            "description": "Project for work item tests",
        },
    )

    assert project_response.status_code == 201

    project = project_response.json()

    # Create a work item belonging to that project.
    response = client.post(
        "/api/work-items",
        json={
            "project_id": project["id"],
            "title": "Build dashboard",
            "description": "Create the initial dashboard",
            "priority": "high",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["project_id"] == project["id"]
    assert data["title"] == "Build dashboard"
    assert data["description"] == "Create the initial dashboard"
    assert data["priority"] == "high"
    assert data["status"] == "todo"
