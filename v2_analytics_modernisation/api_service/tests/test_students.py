from fastapi.testclient import TestClient
from api_service.app.main import app

client = TestClient(app)

def test_students_list():
    r = client.get("/students")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
