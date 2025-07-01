import pytest
from app import create_app, db
from app.models import User, Product, ChatSession, ChatMessage
from test_config import TestConfig
from datetime import datetime

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(TestConfig)

    # Create tables
    with app.app_context():
        db.create_all()

    yield app

    # Clean up
    TestConfig.cleanup()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def init_database(app):
    """Initialize test database with sample data."""
    with app.app_context():
        # Create test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)

        # Create test products
        products = [
            Product(
                name='Test Product 1',
                description='Description for product 1',
                price=99.99,
                category='Electronics',
                stock=10,
                image_url='https://example.com/image1.jpg'
            ),
            Product(
                name='Test Product 2',
                description='Description for product 2',
                price=49.99,
                category='Books',
                stock=20,
                image_url='https://example.com/image2.jpg'
            ),
            Product(
                name='Test Product 3',
                description='Description for product 3',
                price=149.99,
                category='Electronics',
                stock=5,
                image_url='https://example.com/image3.jpg'
            )
        ]
        for product in products:
            db.session.add(product)

        # Create test chat session
        chat_session = ChatSession(
            session_id='test-session-id',
            user_id=1,
            is_active=True,
            created_at=datetime.utcnow()
        )
        db.session.add(chat_session)

        # Create test chat messages
        messages = [
            ChatMessage(
                user_id=1,
                content='Hello, I need help',
                message_type='user',
                session_id='test-session-id',
                timestamp=datetime.utcnow()
            ),
            ChatMessage(
                user_id=None,
                content='Hi! How can I assist you today?',
                message_type='bot',
                session_id='test-session-id',
                timestamp=datetime.utcnow()
            )
        ]
        for message in messages:
            db.session.add(message)

        db.session.commit()

@pytest.fixture
def auth_headers(client):
    """Get authentication headers for test user."""
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}