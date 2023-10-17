from sqlalchemy.orm import Session
from datetime import datetime
from datetime import timedelta
from utils import auth, consts
from models import token_model


def delete_oldest_token(db: Session, user_id: int):
    now = datetime.utcnow()
    db_token_to_delete = db.query(token_model.Token).filter(token_model.Token.user_id == user_id).filter(
        token_model.Token.refresh_token_expiration > now).order_by(token_model.Token.refresh_token_expiration).first()
    if db_token_to_delete:
        db.query(token_model.Token).filter(token_model.Token.id == db_token_to_delete.id).delete()


def get_number_tokens(db: Session, user_id: int):
    now = datetime.utcnow()
    query = db.query(token_model.Token).filter(token_model.Token.user_id == user_id).filter(
        token_model.Token.refresh_token_expiration > now)
    return query.count()


def get_tokens_by_user_id(db: Session, user_id: int):
    query = db.query(token_model.Token).filter(token_model.Token.user_id == user_id)
    return query.order_by(token_model.Token.access_token_expiration.desc()).all()


def get_recent_token_by_user_id(db: Session, user_id: int):
    query = db.query(token_model.Token).filter(token_model.Token.user_id == user_id)
    return query.order_by(token_model.Token.access_token_expiration.desc()).first()


def create_token(db: Session,
                 user_id: int,
                 access_token: str = None,
                 access_token_expiration: str = None,
                 refresh_token: str = None,
                 refresh_token_expiration: str = None
                 ):
    created_at = datetime.utcnow()
    db_token = token_model.Token(
        user_id=user_id,
        access_token=access_token,
        access_token_expiration=access_token_expiration,
        refresh_token=refresh_token,
        refresh_token_expiration=refresh_token_expiration,
        created_at=created_at
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def create_access_token(db: Session,
                        user_id: int):

    access_token_expiration = datetime.utcnow() + timedelta(minutes=consts.Consts.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_token()
    refresh_token_expiration = datetime.utcnow() + timedelta(days=consts.Consts.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = auth.create_token()

    nb_tokens = get_number_tokens(db=db, user_id=user_id)
    if nb_tokens >= consts.Consts.MAX_TOKENS_PER_USER:
        delete_oldest_token(db=db, user_id=user_id)

    db_token = create_token(db=db,
                            user_id=user_id,
                            access_token=access_token,
                            access_token_expiration=access_token_expiration,
                            refresh_token=refresh_token,
                            refresh_token_expiration=refresh_token_expiration
                            )
    return db_token


def get_token_by_access_token(db: Session, token: str):
    now = datetime.utcnow()
    query = db.query(token_model.Token).filter(token_model.Token.access_token == token).filter(
        token_model.Token.access_token_expiration > now)
    return query.first()


def get_token_by_refresh_token(db: Session, token: str):
    now = datetime.utcnow()
    query = db.query(token_model.Token).filter(token_model.Token.refresh_token == token).filter(
        token_model.Token.refresh_token_expiration > now)
    return query.first()


def update_access_and_refresh_tokens(db: Session, refresh_token: str):
    db_token = get_token_by_refresh_token(db=db, token=refresh_token)

    access_token = auth.create_token()
    refresh_token = auth.create_token()
    access_token_expiration = datetime.utcnow() + timedelta(minutes=consts.Consts.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expiration = datetime.utcnow() + timedelta(days=consts.Consts.REFRESH_TOKEN_EXPIRE_DAYS)

    db_token.access_token = access_token
    db_token.access_token_expiration = access_token_expiration
    db_token.refresh_token = refresh_token
    db_token.refresh_token_expiration = refresh_token_expiration

    db.commit()
    return db_token


def logout(db: Session, user_id: int, access_token: str = None):
    query = db.query(token_model.Token).filter(token_model.Token.user_id == user_id)
    if access_token:
        query = query.filter(token_model.Token.access_token == access_token)
    query.delete()


def delete_expired_tokens(db: Session):
    now = datetime.utcnow()
    deleted_count = db.query(token_model.Token).filter(token_model.Token.refresh_token_expiration < now).delete()
    return deleted_count
