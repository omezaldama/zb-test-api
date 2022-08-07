from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from controllers.products import ProductsController
from pd_models.products import Product, ProductCreate, ProductUpdate
from db_models.users import User as DBUser
from dependencies.database import get_db
from utils.auth import get_request_user, raise_401_exception, raise_403_exception


router = APIRouter()

@router.get('/products/', response_model=List[Product])
def get_products(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return ProductsController.get_products(db, skip, limit)

@router.get('/products/{product_id}', response_model=Product)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    request_user: DBUser = Depends(get_request_user)
):
    product = ProductsController.get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail='Product not found')
    if request_user is None:
        update_data = ProductUpdate(anonymous_views=product.anonymous_views + 1)
        ProductsController.update_product(db, product_id, update_data)
    return product

@router.post('/products/', response_model=Product, status_code=201)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    request_user: DBUser = Depends(get_request_user)
):
    if request_user is None:
        raise_401_exception('Please login to use this endpoint')
    if request_user.is_admin():
        return ProductsController.create_product(db, product)
    raise_403_exception('Only admins can create products')

@router.put('/products/{product_id}', response_model=Product)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    request_user: DBUser = Depends(get_request_user)
):
    if request_user is None:
        raise_401_exception('Please login to use this endpoint')
    if request_user.is_admin():
        updated_product = ProductsController.update_product(db, product_id, product)
        if updated_product is None:
            raise HTTPException(status_code=404, detail='Product not found')
        ProductsController.notify_product_update(db, product, product_id, request_user.id)
        return updated_product
    raise_403_exception('Only admins can edit products')

@router.delete('/products/{product_id}', response_model=Product)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    request_user: DBUser = Depends(get_request_user)
):
    if request_user is None:
        raise_401_exception('Please login to use this endpoint')
    if request_user.is_admin():
        deleted_product = ProductsController.delete_product(db, product_id)
        if deleted_product is None:
            raise HTTPException(status_code=404, detail='Product not found')
        return deleted_product
    raise_403_exception('Only admins can delete products')
