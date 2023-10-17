from sqlalchemy.orm import Session
from models import version_model as model


def get_version(db: Session, version: str):
    return db.query(model.Version).filter(model.Version.version == version).first()


def list_versions(db: Session):
    return db.query(model.Version).all()
