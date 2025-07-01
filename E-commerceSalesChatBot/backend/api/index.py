from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json
import time
import random
import sys
import os

# Add the parent directory to the path to import mock_data
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"], 
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], supports_credentials=False)

# Import the real product data from mock_data.py
try:
    from mock_data import generate_products
    # Generate products with images
    sample_products = generate_products(100)  # Generate 100 products with images
    # Add IDs and ratings to products
    for i, product in enumerate(sample_products):
        product['id'] = i + 1
        product['rating'] = round(3.5 + (random.random() * 1.5), 1)  # Random rating between 3.5-5.0
    print(f"Loaded {len(sample_products)} products with images and ratings")
except ImportError:
    # Fallback to simple products if mock_data import fails
    sample_products = [
        {"id": 1, "name": "iPhone 15 Pro", "price": 999.99, "category": "Electronics", "stock": 50, "rating": 4.8, "image_url": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=400&fit=crop"},
        {"id": 2, "name": "MacBook Pro M3", "price": 1999.99, "category": "Electronics", "stock": 30, "rating": 4.9, "image_url": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400&h=400&fit=crop"},
        {"id": 3, "name": "Samsung Galaxy S24", "price": 899.99, "category": "Electronics", "stock": 45, "rating": 4.6, "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop"},
        {"id": 4, "name": "Clean Code", "price": 42.99, "category": "Books", "stock": 100, "rating": 4.7, "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=400&fit=crop"},
        {"id": 5, "name": "JavaScript: The Good Parts", "price": 34.99, "category": "Books", "stock": 85, "rating": 4.5, "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop"},
        {"id": 6, "name": "Premium Cotton T-Shirt", "price": 24.99, "category": "Clothing", "stock": 200, "rating": 4.2, "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop"},
        {"id": 7, "name": "Classic Denim Jeans", "price": 79.99, "category": "Clothing", "stock": 150, "rating": 4.4, "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop"},
        {"id": 8, "name": "Yoga Mat", "price": 29.99, "category": "Sports & Fitness", "stock": 120, "rating": 4.3, "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=400&fit=crop"},
        {"id": 9, "name": "Smart LED Bulbs", "price": 39.99, "category": "Home & Garden", "stock": 150, "rating": 4.1, "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop"},
        {"id": 10, "name": "Coffee Maker", "price": 89.99, "category": "Home & Garden", "stock": 45, "rating": 4.0, "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=400&fit=crop"},
    ]
    print(f"Using fallback products: {len(sample_products)} products")

@app.route('/')
def home():
    return jsonify({
        'message': 'E-commerce Sales Chatbot API',
        'version': '1.0.0',
        'endpoints': {
            'products': '/api/products',
            'categories': '/api/products/categories',
            'auth': '/api/auth/*',
            'chat': '/api/chat/*'
        }
    })

@app.route('/api/products', methods=['GET', 'OPTIONS'])
@cross_origin()
def get_products():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # Get query parameters
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 12))
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    min_price = float(request.args.get('min_price', 0))
    max_price = float(request.args.get('max_price', 10000))
    sort_by = request.args.get('sort', 'name')
    
    # Filter products
    filtered_products = sample_products.copy()
    
    if category:
        filtered_products = [p for p in filtered_products if p['category'].lower() == category.lower()]
    
    if search:
        search_lower = search.lower()
        filtered_products = [p for p in filtered_products 
                           if search_lower in p['name'].lower() or 
                              search_lower in p.get('description', '').lower()]
    
    # Price filter
    filtered_products = [p for p in filtered_products 
                        if min_price <= p['price'] <= max_price]
    
    # Sort products
    if sort_by == 'price_asc':
        filtered_products.sort(key=lambda x: x['price'])
    elif sort_by == 'price_desc':
        filtered_products.sort(key=lambda x: x['price'], reverse=True)
    elif sort_by == 'name':
        filtered_products.sort(key=lambda x: x['name'])
    
    # Pagination
    total = len(filtered_products)
    start = (page - 1) * limit
    end = start + limit
    paginated_products = filtered_products[start:end]
    
    response_data = {
        'products': paginated_products,
        'total': total,
        'page': page,
        'limit': limit,
        'total_pages': (total + limit - 1) // limit
    }
    
    response = jsonify(response_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/products/categories', methods=['GET', 'OPTIONS'])
@cross_origin()
def get_categories():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    categories = list(set(p['category'] for p in sample_products))
    response = jsonify(categories)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Auth endpoints
@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
@cross_origin()
def login():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # Simple mock login
    data = request.get_json() or {}
    # Accept both 'email' and 'username' fields
    email = data.get('email', '') or data.get('username', '')
    password = data.get('password', '')
    
    # Mock authentication - accept any email/username and password for testing
    if email and password:
        mock_user = {
            'id': 1,
            'email': email,
            'name': email.split('@')[0].title(),
            'created_at': '2024-01-01T00:00:00Z'
        }
        mock_token = 'mock_jwt_token_12345'
        
        response = jsonify({
            'message': 'Login successful',
            'user': mock_user,
            'access_token': mock_token
        })
    else:
        response = jsonify({
            'message': 'Email and password are required'
        }), 400
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
@cross_origin()
def register():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # Simple mock registration
    data = request.get_json() or {}
    email = data.get('email', '')
    password = data.get('password', '')
    name = data.get('name', '')
    
    if email and password and name:
        mock_user = {
            'id': 2,
            'email': email,
            'name': name,
            'created_at': '2024-01-01T00:00:00Z'
        }
        mock_token = 'mock_jwt_token_67890'
        
        response = jsonify({
            'message': 'Registration successful',
            'user': mock_user,
            'access_token': mock_token
        })
    else:
        response = jsonify({
            'message': 'Name, email and password are required'
        }), 400
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/auth/profile', methods=['GET', 'OPTIONS'])
@cross_origin()
def profile():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # Mock profile endpoint
    auth_header = request.headers.get('Authorization', '')
    if auth_header and 'mock_jwt_token' in auth_header:
        mock_user = {
            'id': 1,
            'email': 'user@example.com',
            'name': 'Test User',
            'created_at': '2024-01-01T00:00:00Z'
        }
        response = jsonify(mock_user)
    else:
        response = jsonify({'message': 'Unauthorized'}), 401
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Chat endpoints
@app.route('/api/chat/start', methods=['POST', 'OPTIONS'])
@cross_origin()
def start_chat():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # Mock chat session start
    import uuid
    session_id = str(uuid.uuid4())
    
    response = jsonify({
        'session_id': session_id,
        'message': 'Chat session started successfully'
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/chat/message', methods=['POST', 'OPTIONS'])
@cross_origin()
def send_message():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # Mock chat message response
    data = request.get_json() or {}
    user_content = data.get('content', '')
    session_id = data.get('session_id', '')
    
    if user_content:
        # Simple mock bot responses
        bot_responses = [
            "I'd be happy to help you find the perfect product! What are you looking for?",
            "Based on your request, I can recommend some great options from our catalog.",
            "Let me search our products for you. What's your budget range?",
            "That's a great choice! Would you like to see similar products?",
            "I can help you compare different options. What features are most important to you?"
        ]
        
        bot_content = random.choice(bot_responses)
        
        user_message = {
            'id': f'user_{int(time.time() * 1000)}',
            'content': user_content,
            'message_type': 'user',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'session_id': session_id
        }
        
        bot_message = {
            'id': f'bot_{int(time.time() * 1000) + 1}',
            'content': bot_content,
            'message_type': 'bot',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'session_id': session_id
        }
        
        response = jsonify({
            'user_message': user_message,
            'bot_message': bot_message
        })
    else:
        response = jsonify({'message': 'Content is required'}), 400
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Vercel serverless function handler
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Server will be available at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
