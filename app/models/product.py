from sqlalchemy import Column, Integer, String, Float
from app.database import BaseModel

class ProductModel(BaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)
