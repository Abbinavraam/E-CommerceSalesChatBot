import requests
import time

def test_new_server():
    # Wait for server to start
    time.sleep(3)
    
    base_url = 'http://localhost:5000'
    
    print("Testing new server without SocketIO...")
    
    # Test root endpoint
    print("1. Testing root endpoint:")
    response = requests.get(f'{base_url}/')
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        print(f'   Response: {response.json()}')
    
    # Test products endpoint
    print("\n2. Testing products endpoint:")
    response = requests.get(f'{base_url}/api/products?page=1&limit=5')
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'   Products returned: {len(data.get("products", []))}')
        print(f'   Total products: {data.get("total", 0)}')
    else:
        print(f'   Error: {response.text[:200]}')
    
    # Test with category filter (the problematic request)
    print("\n3. Testing with category filter:")
    response = requests.get(f'{base_url}/api/products?page=1&limit=12&category=Electronics&sort=name&search=&min_price=0&max_price=1000')
    print(f'   Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'   Products returned: {len(data.get("products", []))}')
        print(f'   Total products: {data.get("total", 0)}')
    else:
        print(f'   Error: {response.text[:200]}')

if __name__ == '__main__':
    test_new_server()
