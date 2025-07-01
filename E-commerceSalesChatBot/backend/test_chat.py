import requests
import json
import time

def test_chat_endpoints():
    time.sleep(3)  # Wait for server to start
    
    base_url = 'http://localhost:5000'
    
    print("Testing chat endpoints...")
    
    # Test start chat session
    print("1. Testing start chat session:")
    response = requests.post(f'{base_url}/api/chat/start')
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        session_id = data.get('session_id')
        print(f'   Session ID: {session_id}')
    else:
        print(f'   Error: {response.text}')
        return
    
    # Test send message
    print("\n2. Testing send message:")
    message_data = {
        'content': 'Hello, I need help finding a laptop',
        'session_id': session_id
    }
    response = requests.post(f'{base_url}/api/chat/message', json=message_data)
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'   User message: {data.get("user_message", {}).get("content", "")}')
        print(f'   Bot response: {data.get("bot_message", {}).get("content", "")}')
    else:
        print(f'   Error: {response.text}')
    
    # Test get sessions
    print("\n3. Testing get sessions:")
    response = requests.get(f'{base_url}/api/chat/sessions')
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'   Sessions count: {len(data)}')
    else:
        print(f'   Error: {response.text}')
    
    # Test get chat history
    print("\n4. Testing get chat history:")
    response = requests.get(f'{base_url}/api/chat/history/{session_id}')
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'   History messages: {len(data)}')
    else:
        print(f'   Error: {response.text}')

if __name__ == '__main__':
    test_chat_endpoints()
