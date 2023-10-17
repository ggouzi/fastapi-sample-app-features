from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Request
from models import role_model
from schemas import version_schema
from crud import version_crud
from db.database import engine, get_db
from typing import List
from utils.status import get_responses
import logging

router = APIRouter()
role_model.Base.metadata.create_all(bind=engine)
logger = logging.getLogger()
print = logger.info


@router.get("/versions", response_model=List[version_schema.Version], responses=get_responses([426, 500]), tags=["Versions"], description="List Versions. Permission=None")
def list_versions(request: Request, db: Session = Depends(get_db)):
    db_versions = version_crud.list_versions(db)
    return db_versions
