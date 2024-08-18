
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import BaseModel
from sqlalchemy.orm import relationship

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

    vendor = relationship("VendorModel", back_populates="products")
    category = relationship("CategoryModel", back_populates="products")

    interactions = relationship("UserInteraction", back_populates="product")
