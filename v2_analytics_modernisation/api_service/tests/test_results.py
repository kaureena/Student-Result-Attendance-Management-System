from fastapi.testclient import TestClient
from api_service.app.main import app

client = TestClient(app)

def test_results_endpoint():
    r = client.get("/results", params={"class_name":"BCA-3","subject_name":"DBMS","term":"Term-1"})
    assert r.status_code == 200
    assert isinstance(r.json(), list)
