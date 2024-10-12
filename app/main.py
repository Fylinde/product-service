from fastapi import FastAPI
from app.routes import product_routes as product_router  # Corrected import
from app.database import engine, BaseModel

# Initialize FastAPI with metadata for Swagger
app = FastAPI(
    title="Product Service API",
    description="API documentation for the Product Service, which manages product data and related operations.",
    version="1.0.0",
    openapi_tags=[
        {"name": "products", "description": "Operations related to managing products"},
    ],
)

# Initialize database tables
BaseModel.metadata.create_all(bind=engine)

# Register the product router
app.include_router(product_router.router, prefix="/products", tags=["products"])  # Access the 'router' object

@app.get("/")
def read_root():
    return {"message": "Welcome to the Product Service"}
