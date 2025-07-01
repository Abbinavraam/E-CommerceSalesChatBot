import pytest
from app.models import User

def test_register(client):
    # Test successful registration
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json
    assert response.json['user']['username'] == 'newuser'

    # Test duplicate username
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'email': 'another@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert 'error' in response.json

    # Test invalid email
    response = client.post('/api/auth/register', json={
        'username': 'anotheruser',
        'email': 'invalid-email',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert 'error' in response.json

def test_login(client, init_database):
    # Test successful login
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json
    assert response.json['user']['username'] == 'testuser'

    # Test invalid credentials
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert 'error' in response.json

    # Test missing fields
    response = client.post('/api/auth/login', json={
        'username': 'testuser'
    })
    assert response.status_code == 400
    assert 'error' in response.json

def test_refresh_token(client, auth_headers):
    # Test successful token refresh
    response = client.post('/api/auth/refresh', headers=auth_headers)
    assert response.status_code == 200
    assert 'access_token' in response.json

    # Test with invalid token
    response = client.post('/api/auth/refresh', headers={
        'Authorization': 'Bearer invalid-token'
    })
    assert response.status_code == 422

def test_get_profile(client, auth_headers, init_database):
    # Test successful profile retrieval
    response = client.get('/api/auth/profile', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['username'] == 'testuser'
    assert response.json['email'] == 'test@example.com'

    # Test without authentication
    response = client.get('/api/auth/profile')
    assert response.status_code == 401

def test_password_hashing():
    user = User(username='test', email='test@example.com')
    user.set_password('password123')
    
    assert user.password_hash is not None
    assert user.password_hash != 'password123'
    assert user.check_password('password123')
    assert not user.check_password('wrongpassword')