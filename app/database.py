from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import os

# Base class for models
BaseModel = declarative_base()

# Main production database URL
SQLALCHEMY_DATABASE_URL = settings.effective_database_url

# Define a test database URL (set this URL in your environment variables)
TEST_SQLALCHEMY_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "postgresql+psycopg2://postgres:Sylvian@db:5433/test_product_service_db"
)

# Create a test engine and session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(TEST_SQLALCHEMY_DATABASE_URL))
# Conditionally select the correct database URL
is_testing = os.getenv("TESTING", "0") == "1"  # TESTING=1 indicates test mode
database_url = TEST_SQLALCHEMY_DATABASE_URL if is_testing else SQLALCHEMY_DATABASE_URL

# Create engine for the selected database
engine = create_engine(database_url, connect_args={"check_same_thread": False} if "sqlite" in database_url else {})

# Session factory for production or testing
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency to provide a database session for routes and services.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
