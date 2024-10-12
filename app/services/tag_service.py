from sqlalchemy.orm import Session
from app.crud import category_tags, product_tags
from app.schemas.category_tag import CategoryTagCreate, CategoryTagDelete
from app.schemas.product_tag import ProductTagCreate, ProductTagDelete

def add_category_tag_service(db: Session, category_tag: CategoryTagCreate):
    return category_tags.add_category_tag(db, category_tag)

def remove_category_tag_service(db: Session, category_tag: CategoryTagDelete):
    return category_tags.remove_category_tag(db, category_tag)

def add_product_tag_service(db: Session, product_tag: ProductTagCreate):
    return product_tags.add_product_tag(db, product_tag)

def remove_product_tag_service(db: Session, product_tag: ProductTagDelete):
    return product_tags.remove_product_tag(db, product_tag)
