from typing import Optional, List
from pydantic import BaseModel


class ProductBase(BaseModel):
    sku: Optional[str]
    name: str
    price: Optional[float]
    brand: Optional[str]
    anonymous_views: Optional[int]


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Optional[str]


class ProductUpdateNotification(BaseModel):
    update_info: ProductUpdate
    id: int
    user_id: int
    emails: List[str]


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
