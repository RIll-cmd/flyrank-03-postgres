from fastapi.testclient import TestClient
from app import app


def test_task_lifecycle():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}
        assert client.post("/tasks", json={}).status_code == 400
        created = client.post("/tasks", json={"title": "Buy milk"})
        assert created.status_code == 201
        task = created.json()
        assert task["title"] == "Buy milk" and task["done"] is False
        url = f"/tasks/{task['id']}"
        assert client.put(url, json={"done": True}).json()["done"] is True
        assert client.get(url).json()["title"] == "Buy milk"
        assert client.delete(url).status_code == 204
        assert client.get(url).status_code == 404
