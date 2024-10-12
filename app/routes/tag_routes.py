from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.tag_service import (
    add_category_tag_service, remove_category_tag_service,
    add_product_tag_service, remove_product_tag_service
)
from app.schemas.category_tag import CategoryTagCreate, CategoryTagDelete
from app.schemas.product_tag import ProductTagCreate, ProductTagDelete
from app.database import get_db

router = APIRouter()

# Category tag routes
@router.post("/categories/tags/add", response_model=CategoryTagCreate)
def add_category_tag(category_tag: CategoryTagCreate, db: Session = Depends(get_db)):
    return add_category_tag_service(db, category_tag)

@router.delete("/categories/tags/remove", response_model=CategoryTagDelete)
def remove_category_tag(category_tag: CategoryTagDelete, db: Session = Depends(get_db)):
    tag = remove_category_tag_service(db, category_tag)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

# Product tag routes
@router.post("/products/tags/add", response_model=ProductTagCreate)
def add_product_tag(product_tag: ProductTagCreate, db: Session = Depends(get_db)):
    return add_product_tag_service(db, product_tag)

@router.delete("/products/tags/remove", response_model=ProductTagDelete)
def remove_product_tag(product_tag: ProductTagDelete, db: Session = Depends(get_db)):
    tag = remove_product_tag_service(db, product_tag)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag
