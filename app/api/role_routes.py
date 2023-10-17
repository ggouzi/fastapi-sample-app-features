from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Request
from models import role_model
from schemas import role_schema
from crud import role_crud
from db.database import engine, get_db
from typing import List
from utils import custom_declarators, consts
from utils.status import get_responses
from exceptions.CustomException import CustomException
import logging

router = APIRouter()
role_model.Base.metadata.create_all(bind=engine)
logger = logging.getLogger()
print = logger.info


@router.get("/roles", response_model=List[role_schema.Role], responses=get_responses([426, 500]), tags=["Roles"], description="List Roles. Permission=None")
@custom_declarators.version_check
def list_roles(request: Request, db: Session = Depends(get_db)):
    db_roles = role_crud.list_roles(db)
    return db_roles


@router.get("/roles/{role_id}", response_model=role_schema.Role, tags=["Roles"], responses=get_responses([404, 426, 500]), description="Get a Role. Permission=None")
@custom_declarators.version_check
def get_role(role_id: int, request: Request, db: Session = Depends(get_db)):
    db_role = role_crud.get_role(db, role_id)
    if not db_role:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_404,
            detail=consts.Consts.ROLE_NOT_FOUND,
            info=f"Role {role_id} not found"
        )
    return db_role
