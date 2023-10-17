from sqlalchemy.orm import Session
from crud import user_crud, version_crud, item_crud
from repository import token_repository
from exceptions.VersionException import VersionException
from exceptions.CustomException import CustomException
from utils import consts
from fastapi import Request


def retrieve_token_from_header(request: Request):
    auth_header = request.headers.get(consts.Consts.HEADER_AUTH, None)
    if auth_header:
        return auth_header.replace('Bearer ', '')


def is_authenticated(db: Session, token: str):
    if not token:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_401,
            detail=consts.Consts.NOT_AUTHENTIFIED,
            info="Not augthentified"
        )

    allowed_user = token_repository.get_user_by_access_token(db=db, token=token)
    if not allowed_user:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_401,
            detail=consts.Consts.INVALID_CREDENTIALS,
            info="Could not validate credentials"
        )
    return allowed_user


def is_admin(db: Session, token: str):
    db_connected_user = is_authenticated(db=db, token=token)
    if not user_crud.is_admin(db, db_connected_user.id):
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_403,
            detail=consts.Consts.FORBIDDEN_ACCESS,
            info=f"User {db_connected_user.id} does not have access to this resource"
        )
    return db_connected_user


def is_admin_or_item_owner(db: Session, token: str, item_id: int):
    db_connected_user = is_authenticated(db=db, token=token)
    if user_crud.is_admin(db, db_connected_user.id):
        return db_connected_user

    db_item = item_crud.get_item(db, item_id)
    if not db_item:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_404,
            detail=consts.Consts.ITEM_NOT_FOUND,
            info=f"Item {item_id} not found"
        )
    if db_connected_user.id != db_item.user_id:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_403,
            detail=consts.Consts.FORBIDDEN_ACCESS,
            info=f"User {db_connected_user.id} does not have rights to edit Item {item_id}"
        )
    return db_connected_user


def is_admin_or_user_owner(db: Session, token: str, user_id: int):
    db_connected_user = is_authenticated(db=db, token=token)
    if user_crud.is_admin(db, db_connected_user.id):
        return db_connected_user

    db_user = user_crud.get_user(db, user_id)
    if not db_user:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_404,
            detail=consts.Consts.USER_NOT_FOUND,
            info=f"User {user_id} not found"
        )
    if db_connected_user.id != db_user.id:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_403,
            detail=consts.Consts.FORBIDDEN_ACCESS,
            info=f"User {db_connected_user.id} does not have rights to edit User {user_id}"
        )
    return db_connected_user


def is_version_supported(db: Session, version: str):
    if version is not None:
        db_version = version_crud.get_version(db, version)
        if db_version is None or not db_version.supported:
            raise VersionException(
                status_code=consts.Consts.ERROR_CODE_426,
                detail=consts.Consts.VERSION_NOT_SUPPORTED
            )
