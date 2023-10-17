from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from db.database import Base


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    access_token = Column(String(255), unique=True)
    access_token_expiration = Column(DateTime)
    refresh_token = Column(String(255), unique=True)
    refresh_token_expiration = Column(DateTime)
    created_at = Column(DateTime)
