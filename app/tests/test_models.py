import pytest
from app.models.rating import RatingModel
from app.database import BaseModel as Base, TestingSessionLocal, engine
from app.models.product import ProductModel


# Setting up a test database session
@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)  # Create schema
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Drop schema after tests


@pytest.fixture
def sample_product(db_session):
    """
    Create a sample product for testing purposes.
    """
    product = ProductModel(
        name="Sample Product",
        description="A sample product for testing.",
        seller_price=100.0,
        seller_currency="USD",
        is_in_stock=True,
        total_stock=10,
        brand="Sample Brand",
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


# Test for the RatingModel
def test_rating_model(db_session, sample_product):
    """
    Test creating and persisting a RatingModel instance.
    """
    rating = RatingModel(
        product_id=sample_product.id,
        rating=4.5,
        review="Great product!"
    )
    db_session.add(rating)
    db_session.commit()
    db_session.refresh(rating)

    # Assertions
    assert rating.id is not None
    assert rating.product_id == sample_product.id
    assert rating.rating == 4.5
    assert rating.review == "Great product!"
