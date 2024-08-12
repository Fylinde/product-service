
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
     
    vendor = relationship("VendorModel", back_populates="products")
    interactions = relationship("UserInteraction", back_populates="product")
