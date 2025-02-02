
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import BaseModel as Base
from app.models.rating import RatingModel
# from factories import ProductFactory

# Test database URL
TEST_DATABASE_URL = "postgresql+psycopg2://postgres:Sylvian@db:5433/test_product_service_db"

# Create the test engine and session
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Set up the test database before tests run."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """Provide a database session to tests."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

