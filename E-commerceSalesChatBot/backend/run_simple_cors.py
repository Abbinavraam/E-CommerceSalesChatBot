from flask import Flask
from flask_cors import CORS
from app import create_app

def create_simple_app():
    app = create_app()
    
    # Override CORS with more permissive settings
    CORS(app, 
         origins="*",  # Allow all origins for testing
         allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         supports_credentials=True)
    
    return app

if __name__ == '__main__':
    app = create_simple_app()
    print("Starting Flask server with enhanced CORS...")
    print("Server will be available at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
