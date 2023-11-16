from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Request
from typing import Optional
from models import user_model
from utils.status import Status, get_responses
from schemas import user_schema
from crud import (
    user_crud,
    role_crud,
    token_crud
)
from db.database import engine, get_db
from utils import auth, consts, custom_declarators, rights
from exceptions.CustomException import CustomException
import logging

router = APIRouter()
user_model.Base.metadata.create_all(bind=engine)
logger = logging.getLogger()
print = logger.info


@router.post("/users", response_model=user_schema.UserCreated, status_code=201, responses=get_responses([201, 400, 401, 403, 409, 422, 426, 500]), tags=["Users"], description=f"Create an activated User + Password generated randomly. Permission={consts.Consts.PERMISSION_ADMIN}")
@custom_declarators.version_check
@custom_declarators.permission(permission_string=consts.Consts.PERMISSION_ADMIN)
def create_user_as_admin(user: user_schema.UserCreate, request: Request, db: Session = Depends(get_db)):

    # Check user id exists
    db_user = user_crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_409,
            detail=consts.Consts.USER_ALREADY_EXIST,
            info=f"User with same email {user.username} already exists"
        )

    db_role = role_crud.get_role(db, user.role_id)
    if not db_role:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_400,
            detail=consts.Consts.ROLE_NOT_FOUND,
            info="Role User not found"
        )

    # Generate password:
    password = auth.generate_random_password()

    # Create User
    user_s = user_schema.UserCreate(username=user.username, role_id=db_role.id, password=password)
    created_user = user_crud.create_user(db=db, user=user_s, activated=True)

    created_user.password = password
    return created_user


@router.get("/users/{user_id}", response_model=user_schema.UserPublicInfo, tags=["Users"], responses=get_responses([404, 426, 500]), description="Get a User. Permission=None")
@custom_declarators.version_check
def get_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id)
    if not db_user:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_404,
            detail=consts.Consts.USER_NOT_FOUND,
            info=f"User {user_id} not found"
        )

    return db_user


@router.get("/users", response_model=user_schema.UserPublicInfoList, tags=["Users"], responses=get_responses([426, 500]), description="List Users. Permission=None")
@custom_declarators.version_check
def list_users(request: Request, db: Session = Depends(get_db), username: Optional[str] = None, activated: Optional[bool] = True, page: Optional[int] = 1, limit: Optional[int] = consts.Consts.MAX_RESULTS_PER_PAGE):
    db_users = user_crud.list_users(db=db, username=username, activated=activated, page=page, limit=limit)

    if limit > consts.Consts.MAX_RESULTS_PER_PAGE:
        limit = consts.Consts.MAX_RESULTS_PER_PAGE

    total = user_crud.count_users(db=db, username=username, activated=activated)
    listing = user_schema.UserPublicInfoList(page=page, limit=limit, total=total, users=db_users)
    return listing


@router.patch("/users/{user_id}", response_model=user_schema.UserPublicInfo, tags=["Users"], responses=get_responses([400, 401, 403, 404, 409, 422, 426, 500]), description="Update a User. Permission=Admin or User Owner")
@custom_declarators.version_check
@custom_declarators.permission(permission_string=consts.Consts.PERMISSION_ADMIN_OR_USER_OWNER)
def update_user(user: user_schema.UserUpdate, user_id: int, request: Request, db: Session = Depends(get_db)):
    allowed_user = rights.is_authenticated(db, rights.retrieve_token_from_header(request))

    db_user = user_crud.get_user(db=db, user_id=user_id, activated=None)
    if not db_user:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_404,
            detail=consts.Consts.USER_NOT_FOUND,
            info=f"User {user_id} not found"
        )

    db_role_admin = role_crud.get_role_by_name(db, consts.Consts.ROLE_ADMIN)
    if not db_role_admin:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_400,
            detail=consts.Consts.ROLE_NOT_FOUND,
            info=f"Role {user.role_id} not found"
        )

    if user.role_id:
        db_role_user_to_provide = role_crud.get_role(db, user.role_id)
        if not db_role_user_to_provide:
            raise CustomException(
                db=db,
                status_code=consts.Consts.ERROR_CODE_400,
                detail=consts.Consts.ROLE_NOT_FOUND,
                info=f"Role {user.role_id} not found"
            )
    else:
        db_role_user_to_provide = role_crud.get_role(db, db_user.role_id)

    are_different_users = (allowed_user.id != user_id)
    given_user_role_is_admin = (db_role_user_to_provide.id == db_role_admin.id)
    current_user_role_is_admin = (db_user.role_id == db_role_admin.id)
    current_user_role_is_admin = (allowed_user.role_id == db_role_admin.id)

    # If user is trying to update a different user
    if are_different_users:
        # Raise an error if a non-admin tries to update another user
        if not current_user_role_is_admin:
            raise CustomException(
                db=db,
                status_code=consts.Consts.ERROR_CODE_403,
                detail=consts.Consts.CANNOT_EDIT_USER_NON_ADMIN,
                info=f"User {allowed_user.id} is not admin and thus does not have rights to edit User {user_id}"
            )
        # Raise an error if an admin user tries to update another admin user
        elif given_user_role_is_admin:
            raise CustomException(
                db=db,
                status_code=consts.Consts.ERROR_CODE_403,
                detail=consts.Consts.CANNOT_EDIT_ADMIN_USER,
                info=f"User {allowed_user.id} cannot edit admin User {user_id}"
            )
    else:
        if (given_user_role_is_admin and not current_user_role_is_admin):
            raise CustomException(
                db=db,
                status_code=consts.Consts.ERROR_CODE_403,
                detail=consts.Consts.CANNOT_SET_SELF_ADMIN,
                info=f"User {allowed_user.id} cannot elevate own permissions to Admin"
            )

    if user.activated is not None and user.activated != db_user.activated and not current_user_role_is_admin:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_403,
            detail=consts.Consts.ERROR_CODE_ACTIVATE_AS_NON_ADMIN,
            info="Cannot enable/disable without being an Admin User"
        )

    if user.username:
        db_user = user_crud.get_user_by_username(db, user.username)
        if db_user:
            if db_user.id != user_id:
                raise CustomException(
                    db=db,
                    status_code=consts.Consts.ERROR_CODE_409,
                    detail=consts.Consts.USER_ALREADY_EXIST,
                    info=f"User with same username {user.username} already exists"
                )

    db_user = user_crud.update_user(db, user_id, user)
    logger.info(user.__dict__)
    if not db_user:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_500,
            detail=consts.Consts.FAILED_TO_UPDATE_USER,
            info=f"Error when trying to update User {user_id}"
        )

    return db_user


@router.delete("/users/{user_id}", response_model=Status, tags=["Users"], responses=get_responses([401, 403, 404, 409, 422, 426, 500]), description="Disable a User. Permission=Admin or User Owner")
@custom_declarators.version_check
@custom_declarators.permission(permission_string=consts.Consts.PERMISSION_ADMIN_OR_USER_OWNER)
def disable_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    # Disable account
    token_crud.logout(db, user_id)
    disabled_user = user_crud.disable_account(db, user_id)
    if not disabled_user:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_500,
            detail=consts.Consts.FAILED_TO_DISABLE_USER,
            info=f"Error when trying to disable User {user_id}",
        )

    return Status(detail=f"Disabled User {user_id}")
