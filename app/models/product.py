from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import BaseModel
from datetime import datetime

class ProductModel(BaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Dual pricing system
    seller_price = Column(Float, nullable=False)  # Seller's price in their currency
    seller_currency = Column(String, nullable=False, default="USD")  # Seller's currency
    buyer_price = Column(Float, nullable=True)  # Converted price for buyer
    buyer_currency = Column(String, nullable=True, default="USD")  # Buyer's currency

    # Additional product details
    color = Column(String, nullable=True)
    material = Column(String, nullable=True)
    size = Column(String, nullable=True)
    weight = Column(Float, nullable=True)
    brand = Column(String, nullable=True)
    sku = Column(String, nullable=True)
    image_urls = Column(String, nullable=True)
    video_url = Column(String, nullable=True)
    three_d_model_url = Column(String, nullable=True)
    ar_url = Column(String, nullable=True)

    # Inventory and Stock Tracking fields
    is_in_stock = Column(Boolean, default=True)
    total_stock = Column(Integer, default=0)  # Summarized total stock across warehouses

    # SEO Fields
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(String(255), nullable=True)
    meta_keywords = Column(String(255), nullable=True)

    # Relationships
    tags = relationship(
        "ProductTagModel", back_populates="product", cascade="all, delete-orphan"
    )
    ratings = relationship(
        "RatingModel", back_populates="product", cascade="all, delete-orphan"
    )

    # Timestamp fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
