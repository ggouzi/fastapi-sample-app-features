from sqlalchemy.orm import Session
from schemas import user_schema
from models import user_model, role_model
from datetime import datetime
from utils import auth, consts
from sqlalchemy.sql.expression import true


def get_user(db: Session, user_id: int, activated: bool = True):
    query = db.query(user_model.User).filter(user_model.User.id == user_id)
    if activated is not None:
        query = query.filter(user_model.User.activated == activated)
    return query.first()


def get_user_by_username(db: Session, username: str, activated: bool = True):
    query = db.query(user_model.User).filter(user_model.User.username == username)
    if activated is not None:
        query = query.filter(user_model.User.activated == activated)
    return query.first()


def list_users(db: Session, username: str = None, activated: bool = True, limit: int = True, page: int = True):
    query = db.query(user_model.User)
    if activated is not None:
        query = query.filter(user_model.User.activated == activated)
    if username:
        query = query.filter(user_model.User.username.ilike(f"%{username}%"))
    if limit is not None:
        query = query.limit(limit)
        if page is not None:
            query = query.offset((page - 1) * limit)
    return query.all()


def count_users(db: Session, username: str = None, activated: bool = True):
    query = db.query(user_model.User)
    if activated is not None:
        query = query.filter(user_model.User.activated == activated)
    if username:
        query = query.filter(user_model.User.username.ilike(f"%{username}%"))
    return query.count()


def check_authentication(db: Session, username: str, password: str):
    db_user = db.query(user_model.User).filter(user_model.User.activated == true()).filter(user_model.User.username == username).first()
    if not db_user:
        return None
    if not db_user.hashed_password:  # No password = Registered using a 3rd parth auth service
        return None
    if auth.does_password_match(db_user.salt, db_user.hashed_password, password):
        return db.query(user_model.User).filter(user_model.User.username == username).filter(
            user_model.User.hashed_password == db_user.hashed_password).first()


def create_user(db: Session, user: user_schema.UserCreate, activated: bool = True):
    created_at = datetime.utcnow()
    password_obj = auth.hash_password(user.password)
    db_user = user_model.User(
        username=user.username,
        hashed_password=password_obj.hashed_password,  # Store only the sha512 of the bcrypt output
        salt=password_obj.salt,
        activated=activated,
        role_id=user.role_id,
        created_at=created_at,
        updated_at=None
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    deleted_count = db.query(user_model.User).filter(user_model.User.id == user_id).delete()
    db.commit()
    return deleted_count


def update_user(db: Session, user_id: int, user: user_schema.UserUpdate):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    db_user.updated_at = datetime.utcnow()
    if user.role_id:
        db_user.role_id = user.role_id
    if user.username:
        db_user.username = user.username
    if user.activated is not None:
        db_user.activated = user.activated
    if user.password:
        password_obj = auth.hash_password(user.password)
        db_user.salt = password_obj.salt
        db_user.hashed_password = password_obj.hashed_password
    db.commit()
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()


# Auth
def is_admin(db: Session, user_id: int):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    db_role = db.query(role_model.Role).filter(role_model.Role.name == consts.Consts.ROLE_ADMIN).first()
    return db_role.id == db_user.role_id


def is_user(db: Session, user_id: int):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    db_role = db.query(role_model.Role).filter(role_model.Role.name == consts.Consts.ROLE_USER).first()
    return db_role.id == db_user.role_id


def is_admin_or_user(db: Session, user_id: int):
    return is_admin(db, user_id) or is_user(db, user_id)
