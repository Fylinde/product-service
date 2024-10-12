from pydantic import BaseModel
from typing import List, Optional


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category_id: Optional[int] = None
    sku: Optional[str] = None
    brand: Optional[str] = None


class ProductCreate(ProductBase):
    vendor_id: int  # Adding vendor_id for product creation
    category_id: int  # Ensure category is selected when creating a product
    sku: str
    stock: Optional[int] = 0  # Default stock is 0 when creating the product


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    sku: Optional[str] = None
    stock: Optional[int] = None

    class Config:
        orm_mode = True


class Product(ProductBase):
    id: int
    vendor_id: int
    stock: Optional[int] = 0
    is_in_stock: bool = True  # Flag to indicate if the product is in stock
    image_urls: Optional[List[str]] = None
    video_url: Optional[str] = None
    three_d_model_url: Optional[str] = None
    ar_url: Optional[str] = None

    class Config:
        orm_mode = True


class ProductWithStock(Product):
    """
    This schema will be used to display product details along with its stock across warehouses.
    """
    warehouse_stocks: List[dict]  # This will hold warehouse ID and stock information

class ProductWithDetails(ProductResponse):
    reviews: List[ReviewResponse] = []
    orders: List[OrderResponse] = []
    wishlists: List[WishlistResponse] = []
