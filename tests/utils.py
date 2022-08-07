from controllers.users import UsersController
from db_models.users import User
from pd_models.users import UserCreate
from tests.conftest import TestSessionLocal

def create_test_user(db, email: str, password: str, role: str = 'admin'):
    user_data = UserCreate(email=email, password=password, role=role)
    user: User = UsersController.create_user(db, user_data)
    return user

def get_auth_token(client, email: str, password: str):
    response = client.post('/api/v1/login', data={'username': email, 'password': password})
    token_data = response.json()
    return token_data['access_token']

def create_and_login_user(client, db, email: str, password: str, role: str = 'admin'):
    user = create_test_user(db, email, password, role)
    token = get_auth_token(client, email, password)
    return user, token
