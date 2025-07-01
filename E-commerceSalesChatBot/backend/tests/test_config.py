import os
import tempfile

class TestConfig:
    # Generate a temporary file for SQLite database
    db_fd, db_path = tempfile.mkstemp()
    
    # Test configuration
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test-secret-key'
    JWT_SECRET_KEY = 'test-jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 604800  # 1 week
    
    # Chat configuration
    CHAT_HISTORY_LIMIT = 50
    
    # Product configuration
    PRODUCTS_PER_PAGE = 10
    
    # File upload configuration
    UPLOAD_FOLDER = tempfile.mkdtemp()
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # CORS configuration
    CORS_ORIGINS = ['http://localhost:3000']
    
    @classmethod
    def cleanup(cls):
        """Clean up temporary files after tests"""
        os.close(cls.db_fd)
        os.unlink(cls.db_path)
        os.rmdir(cls.UPLOAD_FOLDER)