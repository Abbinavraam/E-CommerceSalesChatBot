from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required
from app.models import Product
from app import db
from sqlalchemy import or_
from . import bp

@bp.route('/', methods=['GET', 'OPTIONS'])
def get_products():
    # Handle preflight requests
    if request.method == 'OPTIONS':
        response = make_response('', 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    page = request.args.get('page', 1, type=int)
    # Handle both 'per_page' and 'limit' parameters
    per_page = request.args.get('per_page', type=int) or request.args.get('limit', 10, type=int)
    category = request.args.get('category')
    search = request.args.get('search')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort = request.args.get('sort', 'name')

    # Build query
    query = Product.query

    # Apply filters (ignore empty strings)
    if category and category.strip():
        query = query.filter(Product.category == category)
    if search and search.strip():
        search_term = f'%{search}%'
        query = query.filter(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    # Apply sorting
    if sort == 'name':
        query = query.order_by(Product.name.asc())
    elif sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort == 'newest':
        query = query.order_by(Product.id.desc())
    else:
        query = query.order_by(Product.name.asc())  # Default sorting

    # Execute paginated query
    products = query.paginate(page=page, per_page=per_page, error_out=False)

    response_data = {
        'products': [product.to_dict() for product in products.items],
        'total': products.total,
        'pages': products.pages,
        'current_page': products.page,
        'per_page': per_page,
        'has_next': products.has_next,
        'has_prev': products.has_prev
    }

    response = make_response(jsonify(response_data))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())

@bp.route('/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(Product.category).distinct().all()
    return jsonify([category[0] for category in categories if category[0]])

@bp.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Search query is required'}), 400

    search_term = f'%{query}%'
    products = Product.query.filter(
        or_(
            Product.name.ilike(search_term),
            Product.description.ilike(search_term)
        )
    ).limit(10).all()

    return jsonify([product.to_dict() for product in products])

@bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    # This is a simple recommendation system that returns top-rated products
    # In a real system, this would use more sophisticated algorithms
    recommended_products = Product.query.order_by(Product.price.desc()).limit(5).all()
    return jsonify([product.to_dict() for product in recommended_products])

@bp.route('/price-range', methods=['GET'])
def get_price_range():
    min_price = db.session.query(db.func.min(Product.price)).scalar()
    max_price = db.session.query(db.func.max(Product.price)).scalar()
    
    return jsonify({
        'min_price': min_price,
        'max_price': max_price
    })