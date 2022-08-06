from sqlalchemy.orm import Session

from db_models.users import User
from pd_models.users import UserCreate, UserUpdate
from utils.crud import CRUDUtils
from utils.auth import hash_password


class UsersController(object):

    @classmethod
    def get_users(cls, db: Session, skip: int = 0, limit: int = 10):
        return CRUDUtils.get_objects(db, User, skip, limit)
    
    @classmethod
    def get_user_by_id(cls, db: Session, user_id: int):
        return CRUDUtils.get_object_by_id(db, User, user_id)
    
    @classmethod
    def create_user(cls, db: Session, user: UserCreate):
        user.password = hash_password(user.password)
        return CRUDUtils.create_object(db, User, user)
    
    @classmethod
    def update_user(cls, db: Session, user_id: int, user: UserUpdate):
        return CRUDUtils.update_object(db, User, user_id, user)
    
    @classmethod
    def delete_user(cls, db: Session, user_id: int):
        return CRUDUtils.delete_object(db, User, user_id)
    
    @classmethod
    def get_all_admin_users(cls, db: Session):
        return db.query(User).filter(User.role == 'admin').all()
