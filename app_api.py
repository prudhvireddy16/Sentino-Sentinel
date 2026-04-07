from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from pydantic import BaseModel

# 1. Load the AI Model and the Feature List we saved during training
# This ensures the API uses the exact same logic as our experiments
model = joblib.load('sentinel_model.pkl')
features = joblib.load('model_features.pkl')

app = FastAPI(title="Sentino-Sentinel Enterprise Fraud API")

# 2. Define the Request Structure (Senior-level data validation)
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
        # Convert incoming JSON data to a Dataframe
        input_df = pd.DataFrame([data.dict()])
        
        # Order columns exactly as the model expects
        input_df = input_df[features]
        
        # Make the Prediction
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]
        
        return {
            "is_fraud": int(prediction),
            "fraud_probability": round(float(probability), 4),
            "system_action": "BLOCK_TRANSACTION" if prediction == 1 else "APPROVE_TRANSACTION",
            "request_timestamp": pd.Timestamp.now().isoformat()
        }
    except Exception as e:
        # Standard error handling for enterprise APIs
        raise HTTPException(status_code=500, detail=f"Inference Error: {str(e)}")

# Command to run: uvicorn app_api:app --reload