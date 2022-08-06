from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from pd_models.tokens import Token
from dependencies.database import get_db
from utils.auth import authenticate_user, create_access_token, raise_401_exception


router = APIRouter()

@router.post('/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise_401_exception('Incorrect email or password')
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
