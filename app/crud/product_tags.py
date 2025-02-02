from sqlalchemy.orm import Session
from app.models.product_tag import ProductTagModel
from app.schemas.product_tag import ProductTagCreate, ProductTagDelete
from sqlalchemy.orm import aliased
from app.models.product import ProductModel
from typing import List


def add_product_tag(db: Session, product_tag: ProductTagCreate):
    db_product_tag = ProductTagModel(**product_tag.dict())
    db.add(db_product_tag)
    db.commit()
    db.refresh(db_product_tag)
    return db_product_tag

def remove_product_tag(db: Session, product_tag: ProductTagDelete):
    db_product_tag = db.query(ProductTagModel).filter_by(product_id=product_tag.product_id, tag=product_tag.tag).first()
    if db_product_tag:
        db.delete(db_product_tag)
        db.commit()
    return db_product_tag

def get_related_products(db: Session, product_id: int, limit: int = 10) -> List[ProductModel]:
    """
    Fetch products related to a given product by shared tags.
    """
    # Alias the ProductTagModel to handle self-referencing joins
    tag_alias = aliased(ProductTagModel)

    # Query products sharing the same tags as the given product
    related_products = (
        db.query(ProductModel)
        .join(ProductTagModel, ProductTagModel.product_id == ProductModel.id)
        .join(tag_alias, tag_alias.tag == ProductTagModel.tag)
        .filter(tag_alias.product_id == product_id, ProductModel.id != product_id)  # Exclude the product itself
        .distinct()  # Ensure no duplicate products
        .limit(limit)
        .all()
    )

    return related_products

def get_all_tags(db: Session) -> List[str]:
    """
    Fetch all unique tags from the database.
    """
    tags = db.query(ProductTagModel.tag).distinct().all()
    return [tag[0] for tag in tags]  # Extract tags from query result tuples


def get_products_by_tag(db: Session, tag: str) -> List[ProductModel]:
    """
    Fetch products associated with a specific tag.
    """
    return (
        db.query(ProductModel)
        .join(ProductTagModel, ProductTagModel.product_id == ProductModel.id)
        .filter(ProductTagModel.tag == tag)
        .all()
    )
    
def get_flash_deals(db: Session) -> List[ProductModel]:
    """
    Fetch products tagged as 'flash-deal'.
    """
    return (
        db.query(ProductModel)
        .join(ProductTagModel, ProductTagModel.product_id == ProductModel.id)
        .filter(ProductTagModel.tag == "flash-deal")
        .all()
    )
    
def get_new_arrivals(db: Session, limit: int = 10) -> List[ProductModel]:
    """
    Fetch the most recently added products, limited by the specified number.
    """
    return (
        db.query(ProductModel)
        .order_by(ProductModel.created_at.desc())  # Sort by creation date, newest first
        .limit(limit)
        .all()
    )
    

def get_featured_products(db: Session, limit: int = 10) -> List[ProductModel]:
    """
    Fetch featured products from the database, limited by the specified number.
    """
    return (
        db.query(ProductModel)
        .filter(ProductModel.is_featured == True)  # Assuming is_featured is a column
        .limit(limit)
        .all()
    )