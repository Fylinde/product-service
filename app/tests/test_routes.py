from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_product_route(db_session):
    from app.models.product import ProductModel

    # Add a sample product to the test database
    product = ProductModel(
        name="Route Test Product",
        description="Test Description",
        seller_price=120.0,
        seller_currency="USD"
    )
    db_session.add(product)
    db_session.commit()

    # Call the API
    response = client.get(f"/products/{product.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Route Test Product"
