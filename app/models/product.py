from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, ARRAY
from sqlalchemy.orm import relationship
from app.database import BaseModel
from datetime import datetime

class ProductModel(BaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))  # Linking to categories
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
    

    vendor = relationship("VendorModel", back_populates="products")
    #category = relationship("CategoryModel", back_populates="products")

    interactions = relationship("UserInteraction", back_populates="product")

    # New relationship to track stock at different warehouse locations
    # stocks = relationship("ProductStockModel", back_populates="product")

    tags = relationship("ProductTagModel", back_populates="product", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)