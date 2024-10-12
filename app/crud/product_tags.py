from sqlalchemy.orm import Session
from app.models.product_tag import ProductTagModel
from app.schemas.product_tag import ProductTagCreate, ProductTagDelete

def add_product_tag(db: Session, product_tag: ProductTagCreate):
    db_product_tag = ProductTagModel(**product_tag.dict())
    db.add(db_product_tag)
    db.commit()
    db.refresh(db_product_tag)
    return db_product_tag

def remove_product_tag(db: Session, product_tag: ProductTagDelete):
    db_product_tag = db.query(ProductTagModel).filter_by(product_id=product_tag.product_id, tag=product_tag.tag).first()
    if db_product_tag:
        db.delete(db_product_tag)
        db.commit()
    return db_product_tag
