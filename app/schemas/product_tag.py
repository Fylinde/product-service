from pydantic import BaseModel

class ProductTagBase(BaseModel):
    product_id: int
    tag: str

class ProductTagCreate(ProductTagBase):
    pass

class ProductTagDelete(ProductTagBase):
    pass
