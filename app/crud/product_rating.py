from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.rating import RatingModel  # Assuming a RatingModel exists
from typing import Optional, Dict
from app.schemas.rating import RatingCreate
from app.models.product import ProductModel
from typing import List



def get_product_rating(db: Session, product_id: int) -> Optional[Dict[str, float]]:
    """
    Fetch the average rating, total count of ratings, and reviews for a product by its ID.
    """
    # Aggregate ratings for the product
    rating_data = (
        db.query(
            func.avg(RatingModel.rating).label("average"),
            func.count(RatingModel.id).label("count")
        )
        .filter(RatingModel.product_id == product_id)
        .first()
    )

    if rating_data and rating_data.count > 0:
        return {"average": rating_data.average, "count": rating_data.count}
    return None

def add_product_rating(db: Session, product_id: int, rating_data: RatingCreate) -> RatingModel:
    """
    Add a rating for a product.
    """
    rating = RatingModel(product_id=product_id, **rating_data.dict())
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating

def get_top_rated_products(db: Session, limit: int = 10) -> List[ProductModel]:
    """
    Fetch top-rated products from the database.
    """
    return (
        db.query(ProductModel)
        .join(RatingModel, RatingModel.product_id == ProductModel.id)
        .group_by(ProductModel.id)
        .order_by(func.avg(RatingModel.rating).desc())  # Sort by average rating in descending order
        .limit(limit)
        .all()
    )