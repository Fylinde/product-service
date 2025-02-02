from pydantic import BaseModel
from typing import List
from app.schemas.product import ProductDetail


class TagResponse(BaseModel):
    tags: List[str]

class RelatedProductsResponse(BaseModel):
    related_products: List[ProductDetail]
    

class ProductsByTagResponse(BaseModel):
    products: List[ProductDetail]
    


class FlashDealsResponse(BaseModel):
    flash_deals: List[ProductDetail]
    
class NewArrivalsResponse(BaseModel):
    new_arrivals: List[ProductDetail]
    
    

class ProductTagBase(BaseModel):
    """
    Shared properties for Product Tags
    """
    tag: str


class ProductTagCreate(ProductTagBase):
    """
    Schema for creating a new product tag
    """
    product_id: int


class ProductTagDelete(BaseModel):
    """
    Schema for deleting a product tag
    """
    product_id: int
    tag: str


class ProductTagResponse(ProductTagBase):
    """
    Schema for returning a product tag
    """
    id: int

    class Config:
        orm_mode = True