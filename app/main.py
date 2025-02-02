from fastapi import FastAPI
from app.routes.product_routes import router as product_router
from app.routes.tag_routes import router as tag_router
from app.database import engine, BaseModel

# Initialize FastAPI with metadata for Swagger
app = FastAPI(
    title="Product Service API",
    description="API documentation for the Product Service, managing product data and tags.",
    version="1.0.0",
    openapi_tags=[
        {"name": "products", "description": "Operations related to managing products"},
        {"name": "tags", "description": "Operations related to managing product tags"},
    ],
)

# Initialize database tables
BaseModel.metadata.create_all(bind=engine)

# Register the product and tag routers
app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(tag_router, prefix="/tags", tags=["tags"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Product Service"}
