import pytest
from app.utils import admin_required, format_price, validate_product_data, paginate_query, error_response, success_response
from app.models import Product
from functools import wraps
from flask import jsonify

def test_format_price():
    assert format_price(10) == '10.00'
    assert format_price(10.1) == '10.10'
    assert format_price(10.11) == '10.11'
    assert format_price(10.111) == '10.11'
    assert format_price(0) == '0.00'
    assert format_price(-10) == '-10.00'

def test_validate_product_data():
    # Test valid product data
    valid_data = {
        'name': 'Test Product',
        'description': 'Test Description',
        'price': 99.99,
        'category': 'Electronics',
        'stock': 10,
        'image_url': 'https://example.com/image.jpg'
    }
    assert validate_product_data(valid_data) is None

    # Test missing required fields
    invalid_data = {
        'name': 'Test Product',
        'price': 99.99
    }
    with pytest.raises(ValueError):
        validate_product_data(invalid_data)

    # Test invalid price
    invalid_price_data = valid_data.copy()
    invalid_price_data['price'] = -10
    with pytest.raises(ValueError):
        validate_product_data(invalid_price_data)

    # Test invalid stock
    invalid_stock_data = valid_data.copy()
    invalid_stock_data['stock'] = -5
    with pytest.raises(ValueError):
        validate_product_data(invalid_stock_data)

def test_paginate_query(app, init_database):
    with app.app_context():
        query = Product.query
        page = 1
        per_page = 2

        # Test successful pagination
        items, total, pages = paginate_query(query, page, per_page)
        assert len(items) <= per_page
        assert total > 0
        assert pages > 0

        # Test empty page
        items, total, pages = paginate_query(query, 999, per_page)
        assert len(items) == 0
        assert total > 0
        assert pages > 0

        # Test invalid page number
        with pytest.raises(ValueError):
            paginate_query(query, 0, per_page)

        # Test invalid per_page
        with pytest.raises(ValueError):
            paginate_query(query, 1, 0)

def test_error_response():
    # Test error response with default status code
    response = error_response('Test error')
    assert response.status_code == 400
    assert response.json['error'] == 'Test error'

    # Test error response with custom status code
    response = error_response('Test error', 404)
    assert response.status_code == 404
    assert response.json['error'] == 'Test error'

def test_success_response():
    # Test success response with data
    data = {'key': 'value'}
    response = success_response(data)
    assert response.status_code == 200
    assert response.json == data

    # Test success response with custom status code
    response = success_response(data, 201)
    assert response.status_code == 201
    assert response.json == data

def test_admin_required(app, auth_headers):
    # Mock admin check function
    def is_admin():
        return True

    # Create a test route with admin_required decorator
    @app.route('/test-admin', methods=['GET'])
    @admin_required
    def test_admin_route():
        return jsonify({'message': 'Admin access granted'})

    with app.test_client() as client:
        # Test with admin user
        response = client.get('/test-admin', headers=auth_headers)
        assert response.status_code == 200
        assert response.json['message'] == 'Admin access granted'

        # Test without authentication
        response = client.get('/test-admin')
        assert response.status_code == 401

        # Test with non-admin user (mock)
        non_admin_headers = {'Authorization': 'Bearer non-admin-token'}
        response = client.get('/test-admin', headers=non_admin_headers)
        assert response.status_code == 403