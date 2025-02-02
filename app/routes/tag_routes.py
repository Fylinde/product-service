from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product_tag import (
    RelatedProductsResponse,
    TagResponse,
    ProductsByTagResponse,
    FlashDealsResponse,
    NewArrivalsResponse,
)
from app.services.tag_service import (
    fetch_related_products,
    fetch_all_tags,
    fetch_products_by_tag,
    fetch_flash_deals,
    fetch_new_arrivals,
)
from app.schemas.product import ProductsByTypeResponse
from app.services.product_service import fetch_products_by_type
from typing import Optional

router = APIRouter()


@router.get("/products/{product_id}/related", response_model=RelatedProductsResponse)
def fetch_related_products_route(
    product_id: int,
    limit: int = Query(10, ge=1, le=50, description="Limit the number of related products"),
    db: Session = Depends(get_db),
):
    """
    Fetch products related to a given product by ID.
    """
    try:
        related_products = fetch_related_products(db, product_id, limit)
        return {"related_products": related_products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/products/tags", response_model=TagResponse)
def fetch_tags_route(db: Session = Depends(get_db)):
    """
    Fetch all unique product tags.
    """
    try:
        tags = fetch_all_tags(db)
        return {"tags": tags}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/products/by-tag", response_model=ProductsByTagResponse)
def fetch_products_by_tag_route(tag: str, db: Session = Depends(get_db)):
    """
    Fetch products by a specific tag.
    """
    try:
        products = fetch_products_by_tag(db, tag)
        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/products/flash-deals", response_model=FlashDealsResponse)
def fetch_flash_deals_route(db: Session = Depends(get_db)):
    """
    Fetch all products tagged as 'flash-deal'.
    """
    try:
        flash_deals = fetch_flash_deals(db)
        return {"flash_deals": flash_deals}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/products/new-arrivals", response_model=NewArrivalsResponse)
def fetch_new_arrivals_route(
    limit: int = Query(10, ge=1, le=50, description="Limit the number of new arrivals"),
    db: Session = Depends(get_db),
):
    """
    Fetch the most recently added products with an optional limit.
    """
    try:
        new_arrivals = fetch_new_arrivals(db, limit)
        return {"new_arrivals": new_arrivals}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/products/by-type", response_model=ProductsByTypeResponse)
def fetch_products_by_type_route(
    type: str,
    filter: Optional[str] = Query(None, description="Optional filter for the product type"),
    db: Session = Depends(get_db),
):
    """
    Fetch products by type with an optional filter.
    """
    try:
        products = fetch_products_by_type(db, type, filter)
        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
