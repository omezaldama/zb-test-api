from unicodedata import name
from sqlalchemy import Column, Integer, String, Float

from utils.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String)
    name = Column(String, nullable=False)
    price = Column(Float)
    brand = Column(String)
    anonymous_views = Column(Integer, nullable=False, default=0)
