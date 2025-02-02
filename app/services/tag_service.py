from sqlalchemy.orm import Session
from app.crud.product_tags import (
     get_related_products,
     get_all_tags, 
     get_products_by_tag,
     get_flash_deals, 
     get_new_arrivals, 
     get_featured_products
)
from app.schemas.product import ProductDetail
from typing import List



def fetch_related_products(db: Session, product_id: int, limit: int = 10) -> List[ProductDetail]:
    """
    Fetch related products and return them in a serialized format.
    """
    related_products = get_related_products(db, product_id, limit)
    return [ProductDetail.from_orm(product) for product in related_products]

def fetch_all_tags(db: Session) -> List[str]:
    """
    Fetch all tags and return them as a list.
    """
    tags = get_all_tags(db)
    return tags


def fetch_products_by_tag(db: Session, tag: str) -> List[ProductDetail]:
    """
    Fetch products by tag and return them in a serialized format.
    """
    products = get_products_by_tag(db, tag)
    return [ProductDetail.from_orm(product) for product in products]

def fetch_flash_deals(db: Session) -> List[ProductDetail]:
    """
    Fetch flash deal products and return them in a serialized format.
    """
    products = get_flash_deals(db)
    return [ProductDetail.from_orm(product) for product in products]

def fetch_new_arrivals(db: Session, limit: int = 10) -> List[ProductDetail]:
    """
    Fetch the newest products and return them in a serialized format.
    """
    products = get_new_arrivals(db, limit)
    return [ProductDetail.from_orm(product) for product in products]

def fetch_featured_products(db: Session, limit: int = 10) -> List[ProductDetail]:
    """
    Fetch featured products and return them in a serialized format.
    """
    products = get_featured_products(db, limit)
    return [ProductDetail.from_orm(product) for product in products]