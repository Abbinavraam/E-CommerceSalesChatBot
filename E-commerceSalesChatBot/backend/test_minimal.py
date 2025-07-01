import requests
import time

def test_minimal_server():
    time.sleep(3)  # Wait for server to start
    
    base_url = 'http://localhost:5000'
    
    print("Testing minimal server...")
    
    # Test root
    response = requests.get(f'{base_url}/')
    print(f'Root: {response.status_code}')
    
    # Test products
    response = requests.get(f'{base_url}/api/products?page=1&limit=5')
    print(f'Products: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'Products returned: {len(data.get("products", []))}')
    
    # Test the exact problematic request
    response = requests.get(f'{base_url}/api/products?page=1&limit=12&category=&sort=name&search=&min_price=0&max_price=1000')
    print(f'Problematic request: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'Products returned: {len(data.get("products", []))}')

if __name__ == '__main__':
    test_minimal_server()
