from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session
from app.models.product import ProductModel
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.product_stock import ProductStockModel
# Create a new product
def create_product(db: Session, product: ProductCreate):
    db_product = ProductModel(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Retrieve a product by its ID
def get_product_by_id(db: Session, product_id: int):
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()

# Update product details
def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return None
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

# Delete a product
def delete_product(db: Session, product_id: int):
    db_product = get_product_by_id(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False

# Retrieve all products
def get_all_products(db: Session):
    return db.query(ProductModel).all()

# Retrieve product details including stock information from warehouses
def get_product_with_stock(db: Session, product_id: int):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product:
        stock_info = db.query(ProductStockModel).filter(ProductStockModel.product_id == product_id).all()
        return {"product": product, "stock": stock_info}
    return None

# Search products by category
def search_products_by_category(db: Session, category_id: int):
    return db.query(ProductModel).filter(ProductModel.category_id == category_id).all()

# Get products by vendor
def get_products_by_vendor(db: Session, vendor_id: int):
    return db.query(ProductModel).filter(ProductModel.vendor_id == vendor_id).all()

# Filter products by stock availability
def get_products_in_stock(db: Session):
    return db.query(ProductModel).filter(ProductModel.is_in_stock == True).all()
