from sqlalchemy.orm import Session
from app.crud.product_crud import get_product_by_id, get_products, create_product, delete_product
from app.schemas.product import ProductResponse, ProductDetail, ProductCreate
from typing import Optional
from app.models.product import ProductModel
from app.crud.product_crud import get_products_by_category, get_all_colors, get_products_by_brand
from app.crud.product_crud import get_product_pricing, get_products_by_type, get_product_details
from app.utils.currency_converter import convert_currency
from app.schemas.pricing import LocalizedPricingResponse
from typing import List
from app.crud.product_crud import update_product
from app.schemas.product import ProductUpdate
from fastapi.exceptions import HTTPException

def fetch_product_by_id(db: Session, product_id: int) -> Optional[ProductDetail]:
    """
    Fetch product by ID and return a serialized response.
    """
    product = get_product_by_id(db, product_id)
    if not product:
        return None

    # Convert product model to schema for a cleaner response
    return ProductDetail.from_orm(product)

def fetch_products(
    db: Session, 
    page: int = 1, 
    page_size: int = 10, 
    seller_id: Optional[int] = None, 
    category_id: Optional[int] = None
) -> ProductResponse:
    """
    Fetch a list of products and format them for the API response.
    """
    products = get_products(db, page, page_size, seller_id, category_id)
    total_count = db.query(ProductModel).count()  # For pagination purposes

    return ProductResponse(
        products=[ProductDetail.from_orm(product) for product in products],
        total_count=total_count,
        page=page,
        page_size=page_size,
    )

def create_new_product(db: Session, product_data: ProductCreate) -> ProductDetail:
    """
    Create a new product and return a serialized response.
    """
    product = create_product(db, product_data)
    return ProductDetail.from_orm(product)


def remove_product(db: Session, product_id: int) -> bool:
    """
    Remove a product by ID and handle any related business logic.
    Returns True if successfully deleted, otherwise raises an exception.
    """
    success = delete_product(db, product_id)
    if not success:
        raise ValueError(f"Product with ID {product_id} not found or could not be deleted.")
    return success

def fetch_products_by_category(db: Session, category_id: int, page: int = 1, page_size: int = 10) -> ProductResponse:
    """
    Fetch products by category and return a formatted response.
    """
    products = get_products_by_category(db, category_id, page, page_size)
    total_count = db.query(ProductModel).filter(ProductModel.category_id == category_id).count()

    return ProductResponse(
        products=[ProductDetail.from_orm(product) for product in products],
        total_count=total_count,
        page=page,
        page_size=page_size,
    )
    

def get_localized_pricing(
    db: Session, product_id: int, buyer_currency: str, exchange_rate: Optional[dict] = None
) -> LocalizedPricingResponse:
    """
    Fetch localized pricing, optionally using provided exchange rate data.
    """
    product = get_product_pricing(db, product_id)
    if not product:
        raise ValueError(f"Product with ID {product_id} not found.")

    # Use provided exchange rates if available, fallback to backend utility
    if exchange_rate:
        rates = exchange_rate.get("rates", {})
        base_currency = exchange_rate.get("baseCurrency", product.seller_currency)
        localized_price = convert_currency(product.seller_price, product.seller_currency, buyer_currency, base_currency, rates)
    else:
        localized_price = convert_currency(product.seller_price, product.seller_currency, buyer_currency)

    return LocalizedPricingResponse(
        product_id=product.id,
        seller_price=product.seller_price,
        seller_currency=product.seller_currency,
        localized_price=localized_price,
        buyer_currency=buyer_currency
    )


def fetch_all_colors(db: Session) -> List[str]:
    """
    Fetch all unique product colors.
    """
    return get_all_colors(db)


def update_existing_product(db: Session, product_id: int, product_data: ProductUpdate) -> ProductDetail:
    """
    Update a product and return the updated details.
    """
    updated_product = update_product(db, product_id, product_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
    
    return ProductDetail.from_orm(updated_product)

def fetch_products_by_type(db: Session, product_type: str, filter: Optional[str] = None) -> List[ProductDetail]:
    """
    Fetch products by type and return them in a serialized format.
    """
    products = get_products_by_type(db, product_type, filter)
    return [ProductDetail.from_orm(product) for product in products]

def fetch_products_by_brand(db: Session, brand: str) -> List[ProductDetail]:
    """
    Fetch products by brand and return them in a serialized format.
    """
    products = get_products_by_brand(db, brand)
    return [ProductDetail.from_orm(product) for product in products]

def fetch_product_details(db: Session, product_id: int) -> ProductDetail:
    """
    Fetch product details and return them in a serialized format.
    """
    product = get_product_details(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
    return ProductDetail.from_orm(product)

