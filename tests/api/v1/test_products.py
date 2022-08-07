from fastapi.testclient import TestClient

from main import app
from db_models.products import Product
from tests.conftest import TestSessionLocal
from tests.utils import create_and_login_user


client = TestClient(app)

def create_test_product(db, name: str, **kwargs) -> Product:
    product = Product(name=name, **kwargs)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def test_get_products(test_db):
    response = client.get('/api/v1/products')
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 0

    product_name = 'test product'
    db = TestSessionLocal()
    create_test_product(db, name=product_name)
    response = client.get('/api/v1/products')
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 1
    product = products[0]
    assert product['name'] == product_name

def test_get_product_detail(test_db):
    response = client.get('api/v1/products/1')
    assert response.status_code == 404

    db = TestSessionLocal()
    product = create_test_product(db, name='test product')
    assert product.anonymous_views == 0

    response = client.get(f'api/v1/products/{product.id}')
    assert response.status_code == 200
    retrieved_product = response.json()
    assert product.name == retrieved_product['name']
    assert retrieved_product['anonymous_views'] == 1

    _, token = create_and_login_user(client, db, 'admin@example.com', 'abc123')
    response = client.get(f'api/v1/products/{product.id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    retrieved_product = response.json()
    assert retrieved_product['anonymous_views'] == 1

def test_create_product(test_db):
    response = client.post('api/v1/products/', json={'name': 'test product'})
    assert response.status_code == 401

    db = TestSessionLocal()
    user, token = create_and_login_user(client, db, 'admin@example.com', 'abc123')
    headers = {'Authorization': f'Bearer {token}'}
    response = client.post('api/v1/products/', json={'name': 'test product'}, headers=headers)
    assert response.status_code == 201

    user.role = 'not-an-admin'
    db.commit()
    db.refresh(user)
    response = client.post('api/v1/products/', json={'name': 'another test product'}, headers=headers)
    assert response.status_code == 403

def test_update_product(test_db, mocker):
    mock_notify = mocker.patch('controllers.notifications.NotificationsController.notify')

    response = client.put('api/v1/products/1', json={'name': 'test product edit'})
    assert response.status_code == 401

    db = TestSessionLocal()
    user, token = create_and_login_user(client, db, 'admin@example.com', 'abc123')
    headers = {'Authorization': f'Bearer {token}'}
    response = client.put('api/v1/products/1', json={'name': 'test product edit'}, headers=headers)
    assert response.status_code == 404

    product = create_test_product(db, name='test product')
    updated_name = 'test product edit'
    updated_sku = 'sku edit'
    response = client.put(f'api/v1/products/{product.id}', json={'name': updated_name, 'sku': updated_sku}, headers=headers)
    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product['name'] == updated_name
    assert updated_product['sku'] == updated_sku
    assert mock_notify.call_count == 1

    user.role = 'not-an-admin'
    db.commit()
    db.refresh(user)
    response = client.put(f'api/v1/products/{product.id}', json={'name': 'test product edit 2'}, headers=headers)
    assert response.status_code == 403

def test_delete_product(test_db):
    response = client.delete('api/v1/products/1')
    assert response.status_code == 401

    db = TestSessionLocal()
    user, token = create_and_login_user(client, db, 'admin@example.com', 'abc123')
    headers = {'Authorization': f'Bearer {token}'}
    response = client.delete('api/v1/products/1', headers=headers)
    assert response.status_code == 404

    product = create_test_product(db, name='test product')
    user.role = 'not-an-admin'
    db.commit()
    db.refresh(user)
    response = client.delete(f'api/v1/products/{product.id}', headers=headers)
    assert response.status_code == 403

    response = client.get('/api/v1/products')
    products = response.json()
    assert len(products) == 1

    user.role = 'admin'
    db.commit()
    db.refresh(user)
    response = client.delete(f'api/v1/products/{product.id}', headers=headers)
    assert response.status_code == 200

    response = client.get('/api/v1/products')
    products = response.json()
    assert len(products) == 0
