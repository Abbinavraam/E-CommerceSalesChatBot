from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from config import Config

db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins="*", supports_credentials=True)
    # Temporarily disable SocketIO to fix CORS issues
    # socketio.init_app(app,
    #                  cors_allowed_origins=['http://localhost:3000', 'http://localhost:5173', 'http://localhost:5174'],
    #                  logger=False,
    #                  engineio_logger=False,
    #                  async_mode='threading')

    # Add a simple test route
    @app.route('/')
    def hello():
        return {'message': 'Backend server is running!', 'status': 'success'}

    @app.route('/api')
    def api_test():
        return {'message': 'API is working!', 'status': 'success'}

    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.chat import bp as chat_bp
    app.register_blueprint(chat_bp, url_prefix='/api/chat')

    from app.products import bp as products_bp
    app.register_blueprint(products_bp, url_prefix='/api/products')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app