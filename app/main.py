from sqlalchemy.orm import Session

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.database import Base, engine, SessionLocal
from app.api.routes import router
from app.pd_models.users import UserCreate
from app.db_models.users import User
from app.controllers.users import UsersController
from app.dependencies.database import get_db


Base.metadata.create_all(bind=engine)

def create_first_admin():
    db: Session = SessionLocal()
    user_data = UserCreate(email='admin@example.com', role='admin', password='abc123')
    try:
        UsersController.create_user(db, user_data)
    except Exception as e:
        pass
create_first_admin()

app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix='/api')
