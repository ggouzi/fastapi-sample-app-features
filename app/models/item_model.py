from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from db.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
