from sqlalchemy.orm import Session
from app.models.product import ProductModel
from typing import List, Optional
from app.schemas.product import ProductCreate, ProductUpdate

def get_product_by_id(db: Session, product_id: int) -> Optional[ProductModel]:
    """
    Fetch a product by its ID.
    """
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()

def get_products(
    db: Session, 
    page: int = 1, 
    page_size: int = 10, 
    seller_id: Optional[int] = None, 
    category_id: Optional[int] = None
) -> List[ProductModel]:
    """
    Fetch products with optional filtering by seller_id and category_id.
    Pagination is supported.
    """
    query = db.query(ProductModel)
    
    if seller_id:
        query = query.filter(ProductModel.seller_id == seller_id)
    
    if category_id:
        query = query.filter(ProductModel.category_id == category_id)

    return query.offset((page - 1) * page_size).limit(page_size).all()

def create_product(db: Session, product_data: ProductCreate) -> ProductModel:
    """
    Create a new product in the database.
    """
    product = ProductModel(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int) -> bool:
    """
    Delete a product by its ID.
    Returns True if the product was successfully deleted, otherwise False.
    """
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return True
    return False

def get_products_by_category(db: Session, category_id: int, page: int = 1, page_size: int = 10) -> List[ProductModel]:
    """
    Fetch products belonging to a specific category with pagination.
    """
    query = db.query(ProductModel).filter(ProductModel.category_id == category_id)
    return query.offset((page - 1) * page_size).limit(page_size).all()


def get_product_pricing(db: Session, product_id: int) -> Optional[ProductModel]:
    """
    Fetch pricing details for a specific product.
    """
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()


def get_all_colors(db: Session) -> List[str]:
    """
    Fetch all unique colors from the product database.
    """
    colors = db.query(ProductModel.color).distinct().all()
    return [color[0] for color in colors if color[0]]  # Extract and filter non-null colors


def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> ProductModel:
    """
    Update product details in the database.
    """
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        return None

    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

def get_products_by_type(db: Session, product_type: str, filter: Optional[str] = None) -> List[ProductModel]:
    """
    Fetch products filtered by type and optional filter criteria.
    """
    query = db.query(ProductModel).filter(ProductModel.type == product_type)  # Assuming `type` is a column
    
    if filter:
        # Example of applying a generic filter; adjust based on actual use case
        query = query.filter(ProductModel.name.ilike(f"%{filter}%"))

    return query.all()


def get_products_by_brand(db: Session, brand: str) -> List[ProductModel]:
    """
    Fetch products associated with a specific brand.
    """
    return db.query(ProductModel).filter(ProductModel.brand == brand).all()

def get_product_details(db: Session, product_id: int) -> Optional[ProductModel]:
    """
    Fetch detailed information for a specific product by its ID.
    """
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()