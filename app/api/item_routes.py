from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Request
from models import item_model as models
from crud import item_crud
from schemas import item_schema
from db.database import engine, get_db
from utils.status import Status, get_responses
from utils import custom_declarators, rights, consts
from exceptions.CustomException import CustomException
import logging
from typing import Optional


router = APIRouter()
models.Base.metadata.create_all(bind=engine)
logger = logging.getLogger()
print = logger.info


@router.post("/items", response_model=item_schema.ItemResponse, status_code=201, responses=get_responses([201, 401, 403, 409, 422, 426, 500]), tags=["Items"], description="Create an Item object. Permission=User")
@custom_declarators.version_check
@custom_declarators.permission(consts.Consts.PERMISSION_USER)
def create_item(item: item_schema.ItemCreate, request: Request, db: Session = Depends(get_db)):
    allowed_user = rights.is_authenticated(db, rights.retrieve_token_from_header(request))

    # Check item do not already exist
    db_item = item_crud.get_item_by_name(db, name=item.name)
    if db_item:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_409,
            detail=consts.Consts.ITEM_ALREADY_EXISTS,
            info=f"Item {item.name} already exists"
        )

    # Create Item
    db_item = item_crud.create_item(db=db, item=item, user_id=allowed_user.id)
    return db_item


@router.patch("/items/{item_id}", response_model=item_schema.ItemResponse, responses=get_responses([401, 403, 404, 409, 422, 426, 500]), tags=["Items"], description="Update an Item object. Permission=User")
@custom_declarators.version_check
@custom_declarators.permission(consts.Consts.PERMISSION_ADMIN_OR_ITEM_OWNER)
def update_item(item_id: int, item: item_schema.ItemUpdate, request: Request, db: Session = Depends(get_db)):
    # Check item exist
    db_item = item_crud.get_item(db, item_id=item_id)
    if not db_item:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_404,
            detail=consts.Consts.ITEM_NOT_FOUND,
            info=f"Item {item_id} not found"
        )

    db_item = item_crud.get_item_by_name(db, name=item.name)
    if db_item:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_409,
            detail=consts.Consts.ITEM_ALREADY_EXISTS,
            info=f"Item {item.name} already exists"
        )

    # Update Item
    db_item = item_crud.update_item(db=db, item_id=item_id, item=item)
    return db_item


@router.get("/items/{item_id}", response_model=item_schema.ItemResponse, responses=get_responses([401, 403, 404, 426, 500]), tags=["Items"], description="Get an Item. Permission=User")
@custom_declarators.version_check
@custom_declarators.permission(consts.Consts.PERMISSION_USER)
def get_item(item_id: int, request: Request, db: Session = Depends(get_db)):
    # Check item do not already exist
    db_item = item_crud.get_item(db, item_id=item_id)
    if not db_item:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_404,
            detail=consts.Consts.ITEM_NOT_FOUND,
            info=f"Item {item_id} not found"
        )

    return db_item


@router.get("/items", response_model=item_schema.ItemList, responses=get_responses([401, 403, 426, 500]), tags=["Items"], description="List Items. Permission=User")
@custom_declarators.version_check
@custom_declarators.permission(consts.Consts.PERMISSION_USER)
def list_items(request: Request, db: Session = Depends(get_db), name: Optional[str] = None, description: Optional[str] = None, page: Optional[int] = 1, limit: Optional[int] = consts.Consts.MAX_RESULTS_PER_PAGE):
    db_items = item_crud.list_items(db=db, name=name, description=description, page=page, limit=limit)

    if limit > consts.Consts.MAX_RESULTS_PER_PAGE:
        limit = consts.Consts.MAX_RESULTS_PER_PAGE

    total = item_crud.count_items(db=db, name=name, description=description)
    listing = item_schema.ItemList(page=page, limit=limit, total=total, items=db_items)
    return listing


@router.delete("/items/{item_id}", response_model=Status, responses=get_responses([401, 403, 404, 426, 500]), tags=["Items"], description="Delete an Item. Permission=Admin or Item owner")
@custom_declarators.version_check
@custom_declarators.permission(consts.Consts.PERMISSION_ADMIN_OR_ITEM_OWNER)
def delete_item(item_id: int, request: Request, db: Session = Depends(get_db)):

    db_item = item_crud.get_item(db, item_id=item_id)
    if not db_item:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_404,
            detail=consts.Consts.ITEM_NOT_FOUND,
            info=f"Item {item_id} not found"
        )

    delete_count = item_crud.delete_item(db, db_item.id)
    if not delete_count:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_500,
            detail=consts.Consts.FAILED_TO_DELETE_ITEM,
            info=f"Error: Item f{db_item.id} cannot be deleted"
        )

    return Status(detail=f"Deleted Item {db_item.id}")
