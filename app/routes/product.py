from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import Product, ProductCreate
from app.crud.product import create_product, get_products
from typing import List

router = APIRouter()

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    product_id = await create_product(db, product)
    return {**product.dict(), "id": product_id[0]}

@router.get("/", response_model=List[Product])
async def read_products(db: Session = Depends(get_db)):
    products = await get_products(db)
    return products
