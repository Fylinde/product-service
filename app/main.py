from fastapi import FastAPI
from app.routes import router
from app.database import engine, BaseModel
from app.routes import product

app = FastAPI()

#BaseModel.metadata.create_all(bind=engine)

app.include_router(product.router, prefix="/products")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Product Service"}
