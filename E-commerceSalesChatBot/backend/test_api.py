import requests
import json

def test_api():
    base_url = 'http://localhost:5000'
    
    # Test root endpoint
    print("Testing root endpoint...")
    response = requests.get(f'{base_url}/')
    print(f'Status: {response.status_code}')
    print(f'Response: {response.json()}')
    print()
    
    # Test API endpoint
    print("Testing API endpoint...")
    response = requests.get(f'{base_url}/api')
    print(f'Status: {response.status_code}')
    print(f'Response: {response.json()}')
    print()
    
    # Test products endpoint
    print("Testing products endpoint...")
    response = requests.get(f'{base_url}/api/products')
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'Products count: {len(data.get("products", []))}')
        print(f'Total products: {data.get("total", 0)}')
    else:
        print(f'Error: {response.text}')
    print()
    
    # Test categories endpoint
    print("Testing categories endpoint...")
    response = requests.get(f'{base_url}/api/products/categories')
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        categories = response.json()
        print(f'Categories: {categories}')
    else:
        print(f'Error: {response.text}')

if __name__ == '__main__':
    test_api()
