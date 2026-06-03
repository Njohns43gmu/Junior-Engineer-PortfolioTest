from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
import models, schemas

def get_items(db: Session, skip: int = 0, limit: int = 100, order: str = "asc"):
    direction = asc(models.Item.id) if order == "asc" else desc(models.Item.id)
    return db.query(models.Item).order_by(direction).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: schemas.ItemUpdate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db_item.title = item.title
        db_item.description = item.description
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item