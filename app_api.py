import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from pydantic import BaseModel

# 1. Setup Environment and Logging
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# 2. Load Model
model = joblib.load('sentinel_model.pkl')
features = joblib.load('model_features.pkl')

app = FastAPI(title="Sentino-Sentinel Enterprise Fraud API")

class Transaction(BaseModel):
    user_id: int
    merchant_id: int
    amount: float

@app.get("/")
def health_check():
    logger.info("Health check endpoint accessed")
    return {
        "status": "Sentinel Systems Active", 
        "version": "XGBoost-Sentinel-v1",
        "latency_monitoring": "Enabled"
    }

@app.post("/v1/predict")
def predict_transaction(data: Transaction):
    try:
        logger.info(f"Predicting transaction for User: {data.user_id}, Amount: {data.amount}")
        
        input_df = pd.DataFrame([data.model_dump()])
        input_df = input_df[features]
        
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]
        
        result = "BLOCK" if prediction == 1 else "ALLOW"
        logger.warning(f"Decision: {result} | Fraud Prob: {probability:.4f}")
        
        return {
            "is_fraud": int(prediction),
            "fraud_probability": round(float(probability), 4),
            "system_action": f"{result}_TRANSACTION",
            "request_timestamp": pd.Timestamp.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Sentinel Error")