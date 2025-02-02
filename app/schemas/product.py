from pydantic import BaseModel, Field
from typing import List, Optional


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category_id: Optional[int] = None
    sku: Optional[str] = None
    brand: Optional[str] = None


class ProductCreate(BaseModel):
    name: str = Field(..., description="Name of the product")
    description: Optional[str] = Field(None, description="Description of the product")
    seller_price: float = Field(..., description="Price set by the seller")
    seller_currency: str = Field(..., description="Currency for seller price")
    buyer_price: Optional[float] = Field(None, description="Price for the buyer")
    buyer_currency: Optional[str] = Field(None, description="Currency for buyer price")
    is_in_stock: bool = Field(default=True, description="Availability status")
    total_stock: int = Field(default=0, description="Total available stock")
    category_id: Optional[int] = Field(None, description="Category ID")
    seller_id: Optional[int] = Field(None, description="Seller ID")

    class Config:
       from_attributes = True 


class Product(ProductBase):
    id: int
    seller_id: int
    stock: Optional[int] = 0
    is_in_stock: bool = True  # Flag to indicate if the product is in stock
    image_urls: Optional[List[str]] = None
    video_url: Optional[str] = None
    three_d_model_url: Optional[str] = None
    ar_url: Optional[str] = None

    class Config:
        from_attributes = True 


class ProductWithStock(Product):
    """
    This schema will be used to display product details along with its stock across warehouses.
    """
    warehouse_stocks: List[dict]  # This will hold warehouse ID and stock information

class ProductDetail(BaseModel):
    id: int
    name: str
    description: Optional[str]
    seller_price: float
    seller_currency: str
    buyer_price: Optional[float]
    buyer_currency: Optional[str]
    is_in_stock: bool
    total_stock: int

    class Config:
        from_attributes = True 

class ProductResponse(BaseModel):
    products: List[ProductDetail]
    total_count: int
    page: int
    page_size: int
    

class DeleteResponse(BaseModel):
    success: bool
    message: str
    

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the product")
    description: Optional[str] = Field(None, description="Description of the product")
    seller_price: Optional[float] = Field(None, description="Price set by the seller")
    seller_currency: Optional[str] = Field(None, description="Currency for seller price")
    buyer_price: Optional[float] = Field(None, description="Price for the buyer")
    buyer_currency: Optional[str] = Field(None, description="Currency for buyer price")
    is_in_stock: Optional[bool] = Field(None, description="Availability status")
    total_stock: Optional[int] = Field(None, description="Total available stock")

    class Config:
        from_attributes = True 
        

class ProductsByTypeResponse(BaseModel):
    products: List[ProductDetail]
    

class ProductsByBrandResponse(BaseModel):
    products: List[ProductDetail]
    
class ProductDetail(BaseModel):
    id: int
    name: str
    description: str
    seller_price: float
    seller_currency: str
    buyer_price: float
    buyer_currency: str
    is_in_stock: bool
    total_stock: int
    brand: str

    class Config:
        from_attributes = True 