import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
import datetime

# 1. Load environment variables
load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "postgres")
DB_NAME = os.getenv("DB_NAME", "sentino_sentinel_db")

# 2. Build the connection string dynamically
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

# (The rest of your table classes remain the same as before...)
class User(Base):
    __tablename__ = 'dim_users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    account_age_days = Column(Integer)
    risk_score = Column(Float)

class Merchant(Base):
    __tablename__ = 'dim_merchants'
    merchant_id = Column(Integer, primary_key=True)
    merchant_name = Column(String)
    category = Column(String)

class Transaction(Base):
    __tablename__ = 'fact_transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('dim_users.user_id'))
    merchant_id = Column(Integer, ForeignKey('dim_merchants.merchant_id'))
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    is_fraud = Column(Integer) 

if __name__ == "__main__":
    print(f" Connecting to {DB_NAME} as {DB_USER}...")
    Base.metadata.create_all(engine)
    print(" Schema updated securely using environment variables.")
