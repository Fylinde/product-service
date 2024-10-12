from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import BaseModel

# ProductTagModel for tagging system
class ProductTagModel(BaseModel):
    __tablename__ = 'product_tags'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    tag = Column(String(50), nullable=False, index=True)
    tag_weight = Column(Float, default=0.0)  # Tag weight for prioritizing

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product = relationship("ProductModel", back_populates="tags")
