from pydantic import BaseModel

class Vendor(BaseModel):
    id: int
    name: str
    description: str = None
    rating: float = None

    class Config:
        orm_mode = True
