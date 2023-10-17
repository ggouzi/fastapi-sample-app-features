from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Request
from schemas import user_schema, token_schema
from repository import token_repository
from crud import token_crud, user_crud
from db.database import get_db
from utils.status import Status, get_responses
from utils import custom_declarators, rights, consts
from exceptions.CustomException import CustomException
import logging

router = APIRouter()

logger = logging.getLogger()
print = logger.info


@router.post('/auth/token', response_model=token_schema.AuthToken, tags=["Auth"], responses=get_responses([401, 422, 426, 500]), description="Get refresh token. Permission=User")
@custom_declarators.version_check
def login(request: Request, auth: token_schema.AuthLogin, db: Session = Depends(get_db)):
    if auth.username and auth.password:
        db_user = user_crud.check_authentication(db, username=auth.username, password=auth.password)
        if not db_user:
            raise CustomException(
                db=db,
                status_code=consts.Consts.ERROR_CODE_401,
                detail=consts.Consts.INVALID_CREDENTIALS_OR_DISABLED,
                info=f"Cannot find activated User with username {auth.username}"
            )
        return token_repository.create_token(db=db, user_id=db_user.id)


@router.post('/auth/refresh', response_model=token_schema.AuthToken, tags=["Auth"], responses=get_responses([401, 422, 500, 426]), description="Get new access token from refresh token. Permission=User")
@custom_declarators.version_check
def refresh_token(request: Request, refresh: token_schema.AuthRefresh, db: Session = Depends(get_db)):

    current_user = token_repository.get_user_by_refresh_token(db=db, token=refresh.refresh_token, activated=True)
    if current_user is None:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_401,
            detail=consts.Consts.INVALID_CREDENTIALS,
            info=f'Cannot validate credentials from refresh token {refresh.refresh_token}'
        )

    db_token = token_crud.update_access_and_refresh_tokens(db=db, refresh_token=refresh.refresh_token)
    if not db_token:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_401,
            detail=consts.Consts.INVALID_CREDENTIALS,
            info=f'Cannot validate credentials from refresh token {refresh.refresh_token}'
        )

    return token_repository.get_token_output(token=db_token)


@router.get('/auth/me', response_model=user_schema.UserPublicInfo, tags=["Auth"], responses=get_responses([401, 426, 500]), description="Get current user from access token. Permission=User")
@custom_declarators.version_check
def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = rights.retrieve_token_from_header(request)

    current_user = token_repository.get_user_by_access_token(db=db, token=token)
    if current_user is None:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_401,
            detail=consts.Consts.INVALID_CREDENTIALS,
            info=f'Cannot validate credentials from access token {token}'
        )

    return current_user


@router.post("/auth/logout", response_model=Status, tags=["Auth"], responses=get_responses([401, 422, 426, 500]), description="Logout. Permission=User")
@custom_declarators.version_check
def logout(request: Request, db: Session = Depends(get_db)):
    token = rights.retrieve_token_from_header(request)
    current_user = rights.is_authenticated(db, token)

    token_crud.logout(db, current_user.id, token)
    return Status(detail=f"User {current_user.id} successfully logged out")
