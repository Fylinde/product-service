from sqlalchemy.orm import Session
from app.schemas.rating import ProductRatingResponse
from app.crud.product_rating import add_product_rating, get_product_rating, get_top_rated_products
from app.crud.product_crud import get_product_by_id
from app.schemas.rating import RatingCreate, RatingResponse
from fastapi.exceptions import HTTPException
from app.schemas.product import ProductDetail
from typing import List


def fetch_product_rating(db: Session, product_id: int) -> ProductRatingResponse:
    """
    Fetch the product rating data and format the response.
    """
    rating_data = get_product_rating(db, product_id)
    if not rating_data:
        return ProductRatingResponse(average=0, count=0)  # Default values if no ratings

    return ProductRatingResponse(average=rating_data["average"], count=rating_data["count"])

def submit_product_rating(db: Session, product_id: int, rating_data: RatingCreate) -> RatingResponse:
    """
    Add a product rating and validate that the product exists.
    """
    # Ensure the product exists
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")

    # Add the rating
    rating = add_product_rating(db, product_id, rating_data)

    # Return a structured response
    return RatingResponse(
        id=rating.id,
        product_id=rating.product_id,
        rating=rating.rating,
        review=rating.review,
        created_at=rating.created_at
    )
    
def fetch_top_rated_products(db: Session, limit: int = 10) -> List[ProductDetail]:
    """
    Fetch top-rated products and return them in a serialized format.
    """
    products = get_top_rated_products(db, limit)
    return [ProductDetail.from_orm(product) for product in products]