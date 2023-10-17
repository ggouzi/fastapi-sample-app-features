from sqlalchemy.orm import Session
from models import role_model


def get_role(db: Session, role_id: int):
    return db.query(role_model.Role).filter(role_model.Role.id == role_id).first()


def get_role_by_name(db: Session, name: str):
    return db.query(role_model.Role).filter(role_model.Role.name == name).first()


def list_roles(db: Session):
    return db.query(role_model.Role).all()
