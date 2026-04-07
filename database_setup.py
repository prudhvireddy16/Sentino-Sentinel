
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

# 1. Connection String
# Format: postgresql://username:password@localhost:5432/database_name
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/sentino_sentinel_db"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

# 2. DIMENSION TABLE: Users (Senior Architecture: Separating user data)
class User(Base):
    __tablename__ = 'dim_users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    account_age_days = Column(Integer)
    risk_score = Column(Float)

# 3. DIMENSION TABLE: Merchants
class Merchant(Base):
    __tablename__ = 'dim_merchants'
    merchant_id = Column(Integer, primary_key=True)
    merchant_name = Column(String)
    category = Column(String)

# 4. FACT TABLE: Transactions (The core table for ML)
class Transaction(Base):
    __tablename__ = 'fact_transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('dim_users.user_id'))
    merchant_id = Column(Integer, ForeignKey('dim_merchants.merchant_id'))
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    is_fraud = Column(Integer) # 0 = Legit, 1 = Fraud

# 5. Execute creation
print("🚀 Creating Normalized Schema in PostgreSQL...")
Base.metadata.create_all(engine)
print("✅ Database tables created successfully.")