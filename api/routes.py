from fastapi import APIRouter
from api.v1.products import router as products_router
from api.v1.users import router as users_router
from api.v1.auth import router as auth_router


router = APIRouter()
router.include_router(products_router, prefix='/v1', tags=['products'])
router.include_router(users_router, prefix='/v1', tags=['users'])
router.include_router(auth_router, prefix='/v1', tags=['auth'])
