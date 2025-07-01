import pytest
from app.models import Product
from app import db

def test_get_products(client):
    # Test products listing
    response = client.get('/api/products/')
    assert response.status_code == 200
    assert 'items' in response.json
    assert 'total' in response.json
    assert 'pages' in response.json

    # Test pagination
    response = client.get('/api/products/?page=1&per_page=1')
    assert response.status_code == 200
    assert len(response.json['items']) == 1

    # Test category filter
    response = client.get('/api/products/?category=Electronics')
    assert response.status_code == 200
    assert all(item['category'] == 'Electronics' for item in response.json['items'])

    # Test price filter
    response = client.get('/api/products/?min_price=50&max_price=100')
    assert response.status_code == 200
    assert all(50 <= item['price'] <= 100 for item in response.json['items'])

def test_get_product(client, init_database):
    # Test getting existing product
    response = client.get('/api/products/1')
    assert response.status_code == 200
    assert response.json['name'] == 'Test Product 1'

    # Test getting non-existent product
    response = client.get('/api/products/999')
    assert response.status_code == 404

def test_get_categories(client, init_database):
    response = client.get('/api/products/categories')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert 'Electronics' in response.json
    assert 'Books' in response.json

def test_search_products(client, init_database):
    # Test search with matching term
    response = client.get('/api/products/search?q=Test')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert all('Test' in item['name'] for item in response.json)

    # Test search with non-matching term
    response = client.get('/api/products/search?q=NonExistent')
    assert response.status_code == 200
    assert len(response.json) == 0

    # Test search without query parameter
    response = client.get('/api/products/search')
    assert response.status_code == 400

def test_get_recommendations(client, auth_headers, init_database):
    # Test with authentication
    response = client.get('/api/products/recommendations', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0

    # Test without authentication
    response = client.get('/api/products/recommendations')
    assert response.status_code == 401

def test_get_price_range(client, init_database):
    response = client.get('/api/products/price-range')
    assert response.status_code == 200
    assert 'min_price' in response.json
    assert 'max_price' in response.json
    assert response.json['min_price'] <= response.json['max_price']

def test_product_model():
    # Test product model creation and to_dict method
    product = Product(
        name='Test Product',
        description='Test Description',
        price=99.99,
        category='Test Category',
        stock=10,
        image_url='https://example.com/image.jpg'
    )

    product_dict = product.to_dict()
    assert product_dict['name'] == 'Test Product'
    assert product_dict['price'] == 99.99
    assert product_dict['category'] == 'Test Category'
    assert product_dict['stock'] == 10