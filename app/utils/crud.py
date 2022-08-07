from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.utils.database import Base


class CRUDUtils(object):

    @classmethod
    def get_objects(cls, db: Session, model: Base, skip: int, limit: int):
        return db.query(model).offset(skip).limit(limit).all()
    
    @classmethod
    def get_object_by_id(cls, db: Session, model: Base, obj_id: int):
        return db.query(model).get(obj_id)
    
    @classmethod
    def create_object(cls, db: Session, model: Base, obj: BaseModel):
        db_object = model(**obj.dict())
        db.add(db_object)
        db.commit()
        db.refresh(db_object)
        return db_object
    
    @classmethod
    def update_object(cls, db: Session, model: Base, obj_id: int, obj: BaseModel):
        db_object = cls.get_object_by_id(db, model, obj_id)
        if db_object is None:
            return None
        for field, value in obj.dict().items():
            if value is not None:
                setattr(db_object, field, value)
        db.add(db_object)
        db.commit()
        db.refresh(db_object)
        return db_object
    
    @classmethod
    def delete_object(cls, db: Session, model: Base, obj_id: int):
        db_object = cls.get_object_by_id(db, model, obj_id)
        if db_object is None:
            return None
        db.delete(db_object)
        db.commit()
        return db_object
