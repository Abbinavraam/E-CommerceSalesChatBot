import pytest
from app.models import ChatMessage, ChatSession
from app import db

def test_start_chat_session(client, auth_headers):
    # Test starting new chat session with authentication
    response = client.post('/api/chat/start', headers=auth_headers)
    assert response.status_code == 200
    assert 'session_id' in response.json
    assert 'message' in response.json

    # Test without authentication
    response = client.post('/api/chat/start')
    assert response.status_code == 401

def test_send_message(client, auth_headers, init_database):
    # Get session ID from init_database
    session_id = 'test-session-id'

    # Test sending valid message
    response = client.post('/api/chat/message', 
        json={
            'content': 'Hello, I need help',
            'session_id': session_id
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    assert 'user_message' in response.json
    assert 'bot_message' in response.json
    assert response.json['user_message']['content'] == 'Hello, I need help'
    assert response.json['bot_message']['message_type'] == 'bot'

    # Test sending message without content
    response = client.post('/api/chat/message',
        json={'session_id': session_id},
        headers=auth_headers
    )
    assert response.status_code == 400

    # Test sending message without session_id
    response = client.post('/api/chat/message',
        json={'content': 'Hello'},
        headers=auth_headers
    )
    assert response.status_code == 400

    # Test with invalid session_id
    response = client.post('/api/chat/message',
        json={
            'content': 'Hello',
            'session_id': 'invalid-session'
        },
        headers=auth_headers
    )
    assert response.status_code == 400

def test_get_chat_history(client, auth_headers, init_database):
    session_id = 'test-session-id'

    # Test getting chat history
    response = client.get(f'/api/chat/history/{session_id}',
        headers=auth_headers
    )
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    assert all(isinstance(msg, dict) for msg in response.json)

    # Test with invalid session_id
    response = client.get('/api/chat/history/invalid-session',
        headers=auth_headers
    )
    assert response.status_code == 200
    assert len(response.json) == 0

    # Test without authentication
    response = client.get(f'/api/chat/history/{session_id}')
    assert response.status_code == 401

def test_get_user_sessions(client, auth_headers, init_database):
    # Test getting user sessions
    response = client.get('/api/chat/sessions',
        headers=auth_headers
    )
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    assert all(isinstance(session, dict) for session in response.json)

    # Test without authentication
    response = client.get('/api/chat/sessions')
    assert response.status_code == 401

def test_chat_models():
    # Test ChatSession model
    session = ChatSession(
        session_id='test-session',
        user_id=1,
        is_active=True
    )
    session_dict = session.to_dict()
    assert session_dict['session_id'] == 'test-session'
    assert session_dict['user_id'] == 1
    assert session_dict['is_active'] is True

    # Test ChatMessage model
    message = ChatMessage(
        user_id=1,
        content='Test message',
        message_type='user',
        session_id='test-session'
    )
    message_dict = message.to_dict()
    assert message_dict['user_id'] == 1
    assert message_dict['content'] == 'Test message'
    assert message_dict['message_type'] == 'user'
    assert message_dict['session_id'] == 'test-session'