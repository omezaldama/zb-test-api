from fastapi.testclient import TestClient

from app.main import app
from app.tests.conftest import TestSessionLocal
from app.tests.utils import create_and_login_user, create_test_user


client = TestClient(app)

def test_get_users(test_db):
    response = client.get('/api/v1/users')
    assert response.status_code == 401

    db = TestSessionLocal()
    email = 'admin@example.com'
    _, token = create_and_login_user(client, db, email, 'abc123')
    response = client.get('/api/v1/users', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 1
    assert users[0]['email'] == email

def test_get_user_detail(test_db):
    response = client.get('/api/v1/users/1')
    assert response.status_code == 401

    db = TestSessionLocal()
    user, token = create_and_login_user(client, db, 'admin@example.com', 'abc123')
    fake_id = user.id + 1
    response = client.get(f'/api/v1/users/{fake_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404

    response = client.get(f'/api/v1/users/{user.id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    retrieved_user = response.json()
    assert retrieved_user['id'] == user.id

    user.role = 'not-an-admin'
    db.commit()
    db.refresh(user)
    response = client.get(f'/api/v1/users/{user.id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 403

def test_create_user(test_db):
    new_user_data = {'email': 'user1@example.com', 'password': 'abc123'}

    response = client.post('/api/v1/users', json=new_user_data)
    assert response.status_code == 401

    db = TestSessionLocal()
    user, token = create_and_login_user(client, db, 'admin@example.com', 'abc123')
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('/api/v1/users', json=new_user_data, headers=headers)
    assert response.status_code == 201
    new_user = response.json()
    assert new_user['email'] == new_user_data['email']

    user.role = 'not-an-admin'
    db.commit()
    db.refresh(user)
    new_user_data['email'] = 'user2@example.com'
    response = client.post('/api/v1/users', json=new_user_data, headers=headers)
    assert response.status_code == 403

def test_update_user(test_db):
    response = client.put('api/v1/users/1', json={'email': 'user2@example.com'})
    assert response.status_code == 401

    db = TestSessionLocal()
    user, token = create_and_login_user(client, db, 'admin@example.com', 'abc123')
    headers = {'Authorization': f'Bearer {token}'}
    fake_id = user.id + 1
    response = client.put(f'api/v1/users/{fake_id}', json={'email': 'user2@example.com'}, headers=headers)
    assert response.status_code == 404

    new_user = create_test_user(db, 'user1@example.com', 'user1pass')
    new_email = 'user2@example.com'
    response = client.put(f'api/v1/users/{new_user.id}', json={'email': new_email}, headers=headers)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user['email'] == new_email

    user.role = 'not-an-admin'
    db.commit()
    db.refresh(user)
    response = client.put(f'api/v1/users/{new_user.id}', json={'email': 'user3@example.com'}, headers=headers)
    assert response.status_code == 403

def test_delete_user(test_db):
    response = client.delete('api/v1/users/1')
    assert response.status_code == 401

    db = TestSessionLocal()
    user, token = create_and_login_user(client, db, 'admin@example.com', 'abc123')
    headers = {'Authorization': f'Bearer {token}'}
    fake_id = user.id + 1
    response = client.delete(f'api/v1/users/{fake_id}', headers=headers)
    assert response.status_code == 404

    new_user = create_test_user(db, 'user1@example.com', 'user1pass')
    user.role = 'not-an-admin'
    db.commit()
    db.refresh(user)
    response = client.delete(f'api/v1/users/{new_user.id}', headers=headers)
    assert response.status_code == 403

    user.role = 'admin'
    db.commit()
    db.refresh(user)
    response = client.delete(f'api/v1/users/{new_user.id}', headers=headers)
    assert response.status_code == 200

    response = client.get('/api/v1/users', headers=headers)
    users = response.json()
    assert len(users) == 1
