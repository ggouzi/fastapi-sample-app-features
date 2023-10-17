from models import user_model
from sqlalchemy.orm import Session
from crud import token_crud
from models import token_model
from utils import consts
from sqlalchemy.sql.expression import true


def create_token(db: Session, user_id: int):
    db_token = token_crud.create_access_token(
        db=db,
        user_id=user_id,
    )
    db_token.expires = consts.Consts.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    db_token.id = db_token.user_id
    return db_token


def get_token_output(token: token_model.Token):
    token.expires = consts.Consts.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    token.id = token.user_id
    return token


def get_user_by_access_token(db: Session, token: str, activated: bool = True):
    db_token = token_crud.get_token_by_access_token(db, token=token)
    if db_token:
        query = db.query(user_model.User).filter(user_model.User.id == db_token.user_id)
        if activated is not None:
            query = query.filter(user_model.User.activated == true())
        return query.first()


def get_user_by_refresh_token(db: Session, token: str, activated: bool = True):
    db_token = token_crud.get_token_by_refresh_token(db, token=token)
    if db_token:
        query = db.query(user_model.User).filter(user_model.User.id == db_token.user_id)
        if activated is not None:
            query = query.filter(user_model.User.activated == true())
        return query.first()
