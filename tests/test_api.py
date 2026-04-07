# tests/test_api.py
from fastapi.testclient import TestClient
from app_api import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Sentinel Systems Active", "model": "XGBoost-v1"}

def test_prediction_endpoint():
    # Test a high amount (Should be Fraud)
    response = client.post("/v1/predict", json={"user_id": 1, "merchant_id": 1, "amount": 5000})
    assert response.status_code == 200
    assert response.json()["is_fraud"] == 1