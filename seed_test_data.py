from app.database import SessionLocal
from app.models.product import ProductModel

def seed_test_data():
    db = SessionLocal()
    try:
        # Add a sample product
        product = ProductModel(
            name="Test Product",
            description="Sample description",
            seller_price=100.0,
            seller_currency="USD",
            buyer_price=110.0,
            buyer_currency="USD"
        )
        db.add(product)
        db.commit()
        print("Seed data added.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_test_data()
