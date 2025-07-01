import pytest
from app import create_app, db
from app.models import User, Product, ChatMessage, ChatSession
from config import TestingConfig

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    # Create test user
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    db.session.add(user)

    # Create test products
    products = [
        Product(
            name='Test Product 1',
            description='Description for test product 1',
            price=99.99,
            category='Electronics',
            stock=10
        ),
        Product(
            name='Test Product 2',
            description='Description for test product 2',
            price=49.99,
            category='Books',
            stock=20
        )
    ]
    db.session.bulk_save_objects(products)

    # Create test chat session
    chat_session = ChatSession(
        session_id='test-session-id',
        user_id=1,
        is_active=True
    )
    db.session.add(chat_session)

    # Create test messages
    messages = [
        ChatMessage(
            user_id=1,
            content='Hello',
            message_type='user',
            session_id='test-session-id'
        ),
        ChatMessage(
            user_id=1,
            content='Hi! How can I help you today?',
            message_type='bot',
            session_id='test-session-id'
        )
    ]
    db.session.bulk_save_objects(messages)

    db.session.commit()

@pytest.fixture
def auth_headers(client, init_database):
    # Login and get token
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}