from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.crud.product_crud import (
    create_product, 
    get_product_by_id, 
    update_product, 
    delete_product, 
    get_all_products, 
    get_product_with_stock,
    search_products_by_category,
    get_products_by_vendor,
    get_products_in_stock
)
from app.utils.rabbitmq import RabbitMQConnection

router = APIRouter()


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    # Create the product
    db_product = create_product(db, product)

    # Publish the product creation event to RabbitMQ
    rabbitmq = RabbitMQConnection(queue_name='product_queue')
    message = {
        "event": "product_created",
        "product_id": db_product.id,
        "name": db_product.name,
        "price": db_product.price,
    }
    rabbitmq.publish_message(message)
    rabbitmq.close_connection()

    return db_product

@router.put("/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
def update_product_route(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    # Update the product
    updated_product = update_product(db, product_id, product)

    # Publish the product update event to RabbitMQ
    rabbitmq = RabbitMQConnection(queue_name='product_queue')
    message = {
        "event": "product_updated",
        "product_id": updated_product.id,
        "name": updated_product.name,
        "price": updated_product.price,
    }
    rabbitmq.publish_message(message)
    rabbitmq.close_connection()

    return updated_product


# Get product details by ID
@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Delete a product
@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    deleted = delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}

# List all products
@router.get("/", response_model=List[Product], status_code=status.HTTP_200_OK)
def list_products_route(db: Session = Depends(get_db)):
    products = get_all_products(db)
    return products

# Get product details along with stock information from warehouses
@router.get("/{product_id}/stock", response_model=Product)
def get_product_with_stock_route(product_id: int, db: Session = Depends(get_db)):
    product_with_stock = get_product_with_stock(db, product_id)
    if not product_with_stock:
        raise HTTPException(status_code=404, detail="Product or stock not found")
    return product_with_stock

# Search products by category
@router.get("/category/{category_id}", response_model=List[Product], status_code=status.HTTP_200_OK)
def search_products_by_category_route(category_id: int, db: Session = Depends(get_db)):
    products = search_products_by_category(db, category_id)
    return products

# List products by vendor
@router.get("/vendor/{vendor_id}", response_model=List[Product], status_code=status.HTTP_200_OK)
def get_products_by_vendor_route(vendor_id: int, db: Session = Depends(get_db)):
    products = get_products_by_vendor(db, vendor_id)
    return products

# List all products that are currently in stock
@router.get("/in-stock", response_model=List[Product], status_code=status.HTTP_200_OK)
def get_products_in_stock_route(db: Session = Depends(get_db)):
    products = get_products_in_stock(db)
    return products
