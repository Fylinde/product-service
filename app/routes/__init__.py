from fastapi import APIRouter
from app.routes.product_routes import router as product_router
from app.routes.tag_routes import router as tag_router

router = APIRouter()



router.include_router(product_router, prefix="/products", tags=["products"])
router.include_router(tag_router, prefix="/tags", tags=["tags"])
