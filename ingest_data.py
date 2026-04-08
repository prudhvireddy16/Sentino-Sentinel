import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# 1. Database Connection (Use your Postgres password)
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/sentino_sentinel_db"
engine = create_engine(DATABASE_URL)

def run_enterprise_ingestion(n=10000):
    print(" Starting Senior-Level ETL Pipeline...")

    # --- STEP A: Populate Dimension Tables First ---
    print(" Populating dim_users...")
    users = pd.DataFrame({
        'user_id': range(1, 1001),
        'user_name': [f"User_{i}" for i in range(1, 1001)],
        'account_age_days': np.random.randint(1, 2000, 1000),
        'risk_score': np.random.uniform(0, 100, 1000)
    })
    users.to_sql('dim_users', engine, if_exists='append', index=False)

    print(" Populating dim_merchants...")
    merchants = pd.DataFrame({
        'merchant_id': range(1, 201),
        'merchant_name': [f"Merchant_{i}" for i in range(1, 201)],
        'category': np.random.choice(['Retail', 'Food', 'Electronics', 'Travel'], 200)
    })
    merchants.to_sql('dim_merchants', engine, if_exists='append', index=False)

    # --- STEP B: Generate Fact Transactions ---
    print(f" Generating {n} enterprise transactions...")
    data = {
        'user_id': np.random.randint(1, 1001, n), # Must be between 1 and 1000
        'merchant_id': np.random.randint(1, 201, n), # Must be between 1 and 200
        'amount': np.random.uniform(5.0, 5000.0, n),
        'is_fraud': 0 
    }
    df = pd.DataFrame(data)

    # Inject Fraud Patterns
    high_value_mask = df['amount'] > 4200
    df.loc[high_value_mask, 'is_fraud'] = np.random.choice([0, 1], size=high_value_mask.sum(), p=[0.2, 0.8])
    
    hacked_merchants = df['merchant_id'].isin([55, 101, 188])
    df.loc[hacked_merchants, 'is_fraud'] = np.random.choice([0, 1], size=hacked_merchants.sum(), p=[0.6, 0.4])

    # --- STEP C: Load Fact Table ---
    print(" Loading data into fact_transactions...")
    df.to_sql('fact_transactions', engine, if_exists='append', index=False)
    
    print("-" * 30)
    print("✅ ETL Successful: All Normalized Tables Populated!")
    print(f"📊 Total Transactions: {len(df)}")
    print(f"🚨 Fraudulent Records: {df['is_fraud'].sum()}")
    print("-" * 30)

if __name__ == "__main__":
    run_enterprise_ingestion()
