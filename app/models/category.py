from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import BaseModel

class CategoryModel(BaseModel):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    trending_score = Column(Float, default=0.0)  # Dynamic scoring field
    popularity_index = Column(Float, default=0.0)  # AI-driven popularity index
    user_interest_score = Column(Float, default=0.0)  # Based on user behavior

    tags = relationship("CategoryTagModel", back_populates="category", cascade="all, delete-orphan")


    # Relationship for parent-child hierarchy
    parent = relationship("CategoryModel", remote_side=[id], backref="subcategories")

    # Relationship with ProductModel
    products = relationship("ProductModel", back_populates="category")
