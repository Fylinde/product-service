from fastapi import FastAPI
from app.routes import router
from app.database import engine, BaseModel

app = FastAPI()

BaseModel.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Product Service"}
