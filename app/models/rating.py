from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import BaseModel
from datetime import datetime

class RatingModel(BaseModel):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    rating = Column(Float, nullable=False)  # Rating value
    review = Column(String, nullable=True)  # Optional review text

    product = relationship("ProductModel", back_populates="ratings")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
