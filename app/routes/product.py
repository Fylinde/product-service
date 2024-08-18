from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.crud.product import create_product, get_product_by_id, update_product, delete_product, get_all_products, get_products, get_product
from typing import List
from app.models.vendor import VendorModel
from app.schemas.vendor import Vendor
from app.models.recommendation import UserInteraction
import logging

router = APIRouter()

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = create_product(db, product)
    return db_product


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
@router.put("/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
def update_product_route(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = get_product_by_id(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = update_product(db, db_product, product)
    return updated_product

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    deleted = delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}


@router.get("/", response_model=List[Product], status_code=status.HTTP_200_OK)
def list_products_route(db: Session = Depends(get_db)):
    products = get_all_products(db)
    return products

@router.get("/{product_id}", response_model=Product)
def get_product_route(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product



