from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aura.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # In production, hash this!
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # User preferences for personalization
    origin_city = Column(String, default="Mumbai")  # Default origin
    preferred_currency = Column(String, default="INR")
    budget_range_min = Column(Float, default=5000)  # Min budget per trip
    budget_range_max = Column(Float, default=50000)  # Max budget per trip
    travel_style = Column(String, default="balanced")  # luxury, budget, balanced
    group_size = Column(Integer, default=2)  # Default number of travelers
    preferred_airlines = Column(JSON, default=list)  # List of preferred airlines
    preferred_hotel_types = Column(JSON, default=list)  # List of preferred hotel types
    dietary_restrictions = Column(JSON, default=list)  # Dietary preferences
    accessibility_needs = Column(JSON, default=list)  # Accessibility requirements

class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    query = Column(Text, nullable=False)
    destination = Column(String)
    search_date = Column(DateTime, default=datetime.utcnow)
    intent = Column(String)  # chat or travel_search
    results_summary = Column(JSON)  # Summary of results returned

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    category = Column(String, nullable=False)  # e.g., "destinations", "activities"
    item = Column(String, nullable=False)  # e.g., "Paris", "beach vacation"
    preference_score = Column(Float, default=1.0)  # How much they like it
    last_updated = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to get a DB session for use in agents (not FastAPI endpoints)
def get_db_session():
    """Get a database session for use outside of FastAPI dependency injection."""
    return SessionLocal()