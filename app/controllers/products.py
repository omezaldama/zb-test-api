from sqlalchemy.orm import Session

from app.db_models.products import Product
from app.pd_models.products import ProductCreate, ProductUpdate, ProductUpdateNotification
from app.controllers.users import UsersController
from app.controllers.notifications import NotificationsController
from app.utils.crud import CRUDUtils


class ProductsController(object):

    @classmethod
    def get_products(cls, db: Session, skip: int = 0, limit: int = 10):
        return CRUDUtils.get_objects(db, Product, skip, limit)
    
    @classmethod
    def get_product_by_id(cls, db: Session, product_id: int):
        return CRUDUtils.get_object_by_id(db, Product, product_id)
    
    @classmethod
    def create_product(cls, db: Session, product: ProductCreate):
        return CRUDUtils.create_object(db, Product, product)
    
    @classmethod
    def update_product(cls, db: Session, product_id: int, product: ProductUpdate):
        return CRUDUtils.update_object(db, Product, product_id, product)
    
    @classmethod
    def delete_product(cls, db: Session, product_id: int):
        return CRUDUtils.delete_object(db, Product, product_id)
    
    @classmethod
    def notify_product_update(cls, db: Session, update_info: ProductUpdate, product_id: int, user_id: int):
        admin_users = UsersController.get_all_admin_users(db)
        admin_emails = list(map(lambda usr: usr.email, admin_users))
        notification_data = ProductUpdateNotification(
            update_info=update_info,
            id=product_id,
            user_id=user_id,
            emails=admin_emails
        )
        NotificationsController('email/product/').notify(notification_data.dict(exclude_none=True))
