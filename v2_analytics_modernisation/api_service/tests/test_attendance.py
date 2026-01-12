from fastapi.testclient import TestClient
from api_service.app.main import app

client = TestClient(app)

def test_attendance_endpoint():
    r = client.get("/attendance", params={"attendance_date":"2026-01-02","class_name":"BCA-3"})
    assert r.status_code == 200
    assert isinstance(r.json(), list)
