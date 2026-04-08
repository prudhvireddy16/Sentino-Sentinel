import pandas as pd
import xgboost as xgb
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import mlflow
import mlflow.xgboost
import joblib

# 1. Connect to PostgreSQL
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/sentino_sentinel_db"
engine = create_engine(DATABASE_URL)

def train_sentinel():
    print(" Starting Advanced ML Training Pipeline...")

    # 2. Extract Data from SQL
    query = "SELECT amount, user_id, merchant_id, is_fraud FROM fact_transactions"
    df = pd.read_sql(query, engine)

    X = df.drop('is_fraud', axis=1)
    y = df['is_fraud']

    # 3. Handle Class Imbalance (The "Senior" Way)
    # Fraud is rare. SMOTE creates synthetic examples so the AI learns better.
    print(" Balancing dataset with SMOTE...")
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

    # 4. MLflow Experiment Tracking
    # This allows you to show a recruiter a history of your AI work.
    mlflow.set_experiment("Sentino_Sentinel_Fraud_Detection")

    with mlflow.start_run():
        print(" Training XGBoost Classifier...")
        
        # Hyperparameters (Adjusting the "dials" of the AI)
        params = {
            "n_estimators": 100,
            "max_depth": 6,
            "learning_rate": 0.1,
            "objective": "binary:logistic",
            "random_state": 42
        }
        
        model = xgb.XGBClassifier(**params)
        model.fit(X_train, y_train)

        # 5. Evaluate (ML Engineers focus on RECALL)
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        # Log to MLflow
        mlflow.log_params(params)
        mlflow.log_metric("accuracy", report['accuracy'])
        mlflow.log_metric("fraud_recall", report['1']['recall'])
        mlflow.xgboost.log_model(model, "model")

        print("-" * 30)
        print(f" Training Complete!")
        print(f" Accuracy: {report['accuracy']:.4f}")
        print(f" Fraud Recall: {report['1']['recall']:.4f}") # How many frauds did we find?
        print("-" * 30)

        # 6. Save locally for production
        joblib.dump(model, 'sentinel_model.pkl')
        joblib.dump(X.columns.tolist(), 'model_features.pkl')
        print(" Model saved as sentinel_model.pkl")

if __name__ == "__main__":
    train_sentinel()
