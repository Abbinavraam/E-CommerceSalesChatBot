from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User

def admin_required(fn):
    """Decorator to check if the current user is an admin"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin privileges required'}), 403
        return fn(*args, **kwargs)
    return wrapper

def format_price(price):
    """Format price to two decimal places"""
    return "{:.2f}".format(float(price))

def validate_product_data(data):
    """Validate product data before creation or update"""
    errors = []
    
    required_fields = ['name', 'price', 'category']
    for field in required_fields:
        if field not in data:
            errors.append(f'{field} is required')
    
    if 'price' in data:
        try:
            price = float(data['price'])
            if price < 0:
                errors.append('Price must be non-negative')
        except ValueError:
            errors.append('Price must be a valid number')
    
    if 'stock' in data:
        try:
            stock = int(data['stock'])
            if stock < 0:
                errors.append('Stock must be non-negative')
        except ValueError:
            errors.append('Stock must be a valid integer')
    
    return errors

def paginate_query(query, page, per_page):
    """Helper function to paginate SQLAlchemy queries"""
    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 10
    
    items = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return {
        'items': [item.to_dict() for item in items.items],
        'total': items.total,
        'pages': items.pages,
        'current_page': items.page
    }

def error_response(message, status_code=400):
    """Helper function to return error responses"""
    return jsonify({'error': message}), status_code

def success_response(data, message=None, status_code=200):
    """Helper function to return success responses"""
    response = {'data': data}
    if message:
        response['message'] = message
    return jsonify(response), status_code