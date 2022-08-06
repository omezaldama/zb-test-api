from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from controllers.users import UsersController
from pd_models.users import User, UserCreate, UserUpdate
from db_models.users import User as DBUser
from dependencies.database import get_db
from utils.auth import get_request_user, raise_401_exception, raise_403_exception


router = APIRouter()

@router.get('/users/', response_model=List[User])
def get_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    request_user: DBUser = Depends(get_request_user)
):
    if request_user is None:
        raise_401_exception('Please login to use this endpoint')
    if request_user.is_admin():
        return UsersController.get_users(db, skip, limit)
    raise_403_exception('Only admins can view users')

@router.get('/users/{user_id}', response_model=User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    request_user: DBUser = Depends(get_request_user)
):
    if request_user is None:
        raise_401_exception('Please login to use this endpoint')
    if request_user.is_admin():
        return UsersController.get_user_by_id(db, user_id)
    raise_403_exception('Only admins can view users')

@router.post('/users/', response_model=User)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    request_user: DBUser = Depends(get_request_user)
):
    if request_user is None:
        raise_401_exception('Please login to use this endpoint')
    if request_user.is_admin():
        return UsersController.create_user(db, user)
    raise_403_exception('Only admins can create users')

@router.put('/users/{user_id}', response_model=User)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    request_user: DBUser = Depends(get_request_user)
):
    if request_user is None:
        raise_401_exception('Please login to use this endpoint')
    if request_user.is_admin():
        return UsersController.update_user(db, user_id, user)
    raise_403_exception('Only admins can edit users')

@router.delete('/users/{user_id}', response_model=User)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    request_user: DBUser = Depends(get_request_user)
):
    if request_user is None:
        raise_401_exception('Please login to use this endpoint')
    if request_user.is_admin():
        return UsersController.delete_user(db, user_id)
    raise_403_exception('Only admins can delete users')
