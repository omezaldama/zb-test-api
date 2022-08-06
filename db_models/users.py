from xmlrpc.client import Boolean
from sqlalchemy import Column, Integer, String

from utils.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="admin")

    def is_admin(self) -> Boolean:
        return self.role == 'admin'
