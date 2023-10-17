from sqlalchemy import Column, Integer, String, Boolean
from db.database import Base


class Version(Base):
    __tablename__ = "versions"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String(16))
    supported = Column(Boolean)
