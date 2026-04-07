from fastapi.testclient import TestClient
from app_api import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "Sentinel Systems Active", 
        "version": "XGBoost-Sentinel-v1",
        "latency_monitoring": "Enabled"
    }

def test_prediction_endpoint():
    response = client.post("/v1/predict", json={"user_id": 1, "merchant_id": 1, "amount": 4900})
    assert response.status_code == 200
    assert response.json()["is_fraud"] == 1