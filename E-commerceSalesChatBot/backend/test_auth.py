import requests
import json
import time

def test_auth_endpoints():
    time.sleep(3)  # Wait for server to start
    
    base_url = 'http://localhost:5000'
    
    print("Testing auth endpoints...")
    
    # Test login
    login_data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    print("1. Testing login:")
    response = requests.post(f'{base_url}/api/auth/login', json=login_data)
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'   User: {data.get("user", {}).get("name")}')
        print(f'   Token: {data.get("token", "")[:20]}...')
        token = data.get("token")
    else:
        print(f'   Error: {response.text}')
        return
    
    # Test profile with token
    print("\n2. Testing profile:")
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{base_url}/api/auth/profile', headers=headers)
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'   Profile: {data.get("name")} ({data.get("email")})')
    else:
        print(f'   Error: {response.text}')
    
    # Test register
    print("\n3. Testing register:")
    register_data = {
        'name': 'New User',
        'email': 'newuser@example.com',
        'password': 'newpassword123'
    }
    response = requests.post(f'{base_url}/api/auth/register', json=register_data)
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'   User: {data.get("user", {}).get("name")}')
        print(f'   Token: {data.get("token", "")[:20]}...')
    else:
        print(f'   Error: {response.text}')

if __name__ == '__main__':
    test_auth_endpoints()
