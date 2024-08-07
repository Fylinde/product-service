from sqlalchemy import insert, select
from app.models.product import ProductModel
from app.schemas.product import ProductCreate, Product
from sqlalchemy.orm import Session

def create_product(db: Session, product: ProductCreate):
    db_product = ProductModel(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(ProductModel).all()
