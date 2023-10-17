from sqlalchemy.orm import Session
from models import item_model as model
from schemas import item_schema as schema
from datetime import datetime


def get_item(db: Session, item_id: int):
    return db.query(model.Item).filter(model.Item.id == item_id).first()


def get_item_by_name(db: Session, name: str):
    return db.query(model.Item).filter(model.Item.name == name).first()


def create_item(db: Session, item: schema.ItemCreate, user_id: int):
    created_at = datetime.utcnow()
    db_item = model.Item(
        name=item.name,
        description=item.description,
        created_at=created_at,
        updated_at=None,
        user_id=user_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item: schema.ItemUpdate):
    db_item = db.query(model.Item).filter(model.Item.id == item_id).first()
    db_item.updated_at = datetime.utcnow()
    if item.name:
        db_item.name = item.name
    if item.description:
        db_item.description = item.description
    db.commit()
    return db.query(model.Item).filter(model.Item.id == item_id).first()


def count_items(db: Session, item_id: int = None, name: str = None, description: str = None):
    query = db.query(model.Item)
    if item_id:
        query = query.filter(model.Item.id == item_id)
    if name:
        query = query.filter(model.Item.name.ilike(f"%{name}%"))
    if description:
        query = query.filter(model.Item.description.ilike(f"%{description}%"))
    return query.count()


def list_items(db: Session, item_id: int = None, name: str = None, description: str = None, limit: int = None, page: int = None):
    query = db.query(model.Item)
    if item_id:
        query = query.filter(model.Item.id == item_id)
    if name:
        query = query.filter(model.Item.name.ilike(f"%{name}%"))
    if description:
        query = query.filter(model.Item.description.ilike(f"%{description}%"))
    if limit is not None:
        query = query.limit(limit)
        if page is not None:
            query = query.offset((page - 1) * limit)
    return query.all()


def delete_item(db: Session, item_id: int):
    deleted_count = db.query(model.Item).filter(model.Item.id == item_id).delete()
    db.commit()
    return deleted_count
