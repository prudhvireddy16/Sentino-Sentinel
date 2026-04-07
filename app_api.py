import logging

# Configure professional logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.Stream_Handler()]
)
logger = logging.getLogger(__name__)
from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from pydantic import BaseModel

# 1. Load the "Brain" and Features
model = joblib.load('sentinel_model.pkl')
features = joblib.load('model_features.pkl')

app = FastAPI(title="Sentino-Sentinel Enterprise Fraud API")

class Transaction(BaseModel):
    user_id: int
    merchant_id: int
    amount: float

@app.get("/")
def health_check():
    return {
        "status": "Sentinel Systems Active", 
        "version": "XGBoost-Sentinel-v1",
        "latency_monitoring": "Enabled"
    }

@app.post("/v1/predict")
def predict_transaction(data: Transaction):
    try:
        # Convert JSON to Dataframe using modern Pydantic model_dump
        input_df = pd.DataFrame([data.model_dump()])
        
        # Ensure columns are in the right order
        input_df = input_df[features]
        
        # Make Prediction
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]
        
        return {
            "is_fraud": int(prediction),
            "fraud_probability": round(float(probability), 4),
            "system_action": "BLOCK_TRANSACTION" if prediction == 1 else "APPROVE_TRANSACTION",
            "request_timestamp": pd.Timestamp.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))