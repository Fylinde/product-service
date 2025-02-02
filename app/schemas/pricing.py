from pydantic import BaseModel

class LocalizedPricingResponse(BaseModel):
    product_id: int
    seller_price: float
    seller_currency: str
    localized_price: float
    buyer_currency: str
