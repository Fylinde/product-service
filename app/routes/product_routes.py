from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.product_service import fetch_product_by_id, fetch_products, create_new_product, remove_product, fetch_products_by_category
from app.schemas.product import ProductResponse, ProductDetail, ProductCreate
from typing import  Optional
from app.schemas.rating import ProductRatingResponse, RatingCreate, RatingResponse, TopRatedProductsResponse
from app.services.product_rating_service import fetch_product_rating, submit_product_rating, fetch_top_rated_products
from app.services.product_service import get_localized_pricing, fetch_product_details
from app.schemas.pricing import LocalizedPricingResponse
from app.services.product_service import fetch_all_colors, update_existing_product, fetch_products_by_type, fetch_products_by_brand
from app.schemas.color import ColorResponse
from app.schemas.product import ProductUpdate, ProductsByTypeResponse, ProductsByBrandResponse




router = APIRouter()

@router.get("/products", response_model=ProductResponse)
def get_products(
    page: int = 1,
    page_size: int = 10,
    seller_id: Optional[int] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Fetch a list of products with optional filtering.
    """
    return fetch_products(db, page, page_size, seller_id, category_id)

@router.get("/products/{product_id}", response_model=ProductDetail)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Fetch a product by its ID.
    """
    product = fetch_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products", response_model=ProductDetail)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.
    """
    try:
        return create_new_product(db, product)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating product: {str(e)}")

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product by its ID.
    """
    try:
        remove_product(db, product_id)
        return {"success": True, "message": f"Product with ID {product_id} deleted successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.get("/products/{product_id}/rating", response_model=ProductRatingResponse)
def get_product_rating(product_id: int, db: Session = Depends(get_db)):
    """
    Fetch the rating details for a product by its ID.
    """
    try:
        return fetch_product_rating(db, product_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    
@router.post("/products/{product_id}/rating", response_model=RatingResponse)
def add_product_rating(product_id: int, rating_data: RatingCreate, db: Session = Depends(get_db)):
    """
    Add a rating to a product.
    """
    try:
        return submit_product_rating(db, product_id, rating_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")  
    
    
@router.get("/products/category/{category_id}", response_model=ProductResponse)
def get_products_by_category(category_id: int, page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    """
    Fetch products by category ID with pagination.
    """
    try:
        return fetch_products_by_category(db, category_id, page, page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")  
    
    
    

@router.get("/products/{product_id}/pricing", response_model=LocalizedPricingResponse)
def get_localized_pricing_route(product_id: int, buyer_currency: str, db: Session = Depends(get_db)):
    """
    Fetch the localized pricing for a product.
    """
    try:
        return get_localized_pricing(db, product_id, buyer_currency)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@router.get("/products/colors", response_model=ColorResponse)
def fetch_colors_route(db: Session = Depends(get_db)):
    """
    Fetch all unique product colors.
    """
    try:
        colors = fetch_all_colors(db)
        return {"colors": colors}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    

@router.put("/products/{product_id}", response_model=ProductDetail)
def update_product_route(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    """
    Update a product by its ID.
    """
    try:
        return update_existing_product(db, product_id, product_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@router.get("/products/by-type", response_model=ProductsByTypeResponse)
def fetch_products_by_type_route(type: str, filter: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Fetch products by type with an optional filter.
    """
    try:
        products = fetch_products_by_type(db, type, filter)
        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")    
    


@router.get("/products/top-rated", response_model=TopRatedProductsResponse)
def fetch_top_rated_products_route(limit: int = 10, db: Session = Depends(get_db)):
    """
    Fetch top-rated products with an optional limit.
    """
    try:
        top_rated_products = fetch_top_rated_products(db, limit)
        return {"top_rated_products": top_rated_products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.get("/products/by-brand", response_model=ProductsByBrandResponse)
def fetch_products_by_brand_route(brand: str, db: Session = Depends(get_db)):
    """
    Fetch products by a specific brand.
    """
    try:
        products = fetch_products_by_brand(db, brand)
        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.get("/products/{product_id}", response_model=ProductDetail)
def fetch_product_details_route(product_id: int, db: Session = Depends(get_db)):
    """
    Fetch detailed information for a specific product by its ID.
    """
    try:
        return fetch_product_details(db, product_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")