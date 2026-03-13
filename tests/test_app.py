import pytest
from app import app

@pytest.fixture
def client():
    """Фикстура для тестового клиента Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """Тест главной страницы"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "Welcome to CI/CD Demo App!"
    assert data['status'] == "ok"
    assert data['version'] == "1.0.0"

def test_health(client):
    """Тест эндпоинта здоровья"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "healthy"
    assert data['version'] == "1.0.0"

def test_users_list(client):
    """Тест списка пользователей"""
    response = client.get('/api/users')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['users']) == 2
    assert data['users'][0]['name'] == "Alice"
    assert data['users'][1]['name'] == "Bob"
    assert data['total'] == 2

def test_get_user(client):
    """Тест получения пользователя по ID"""
    response = client.get('/api/users/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == "Alice"
    
    response = client.get('/api/users/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == "User not found"