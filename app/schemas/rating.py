from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List
from app.schemas.product import ProductDetail


class ProductRatingResponse(BaseModel):
    average: float
    count: int

class RatingCreate(BaseModel):
    rating: float
    review: Optional[str] = None

class RatingResponse(BaseModel):
    id: int
    product_id: int
    rating: float
    review: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
        

class TopRatedProductsResponse(BaseModel):
    top_rated_products: List[ProductDetail]