from fastapi.testclient import TestClient
from .app import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status":"ok"}
    
def test_welcome():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message":"Welcome to FastAPI"
    }
    
def test_query():
    response = client.post(
        "/query",
        params={"query": "What is Kubernetes ?"}
    )
    
    answer = response.json()["answer"]
    
    assert "open-source" in answer
    assert "containerized" in answer
    
def test_add_knowledge():
    response = client.post(
        "/add",
        params={"text": "Paris is the capital of France."}
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Knowledge Base has been updated"