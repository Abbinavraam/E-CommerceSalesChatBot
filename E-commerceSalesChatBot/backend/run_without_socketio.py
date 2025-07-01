from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

# Create Flask app without SocketIO
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()

db.init_app(app)
jwt.init_app(app)

# Configure CORS with very permissive settings
CORS(app, 
     origins="*",  # Allow all origins
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=True)

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

if __name__ == '__main__':
    print("Starting Flask server without SocketIO...")
    print("Server will be available at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
