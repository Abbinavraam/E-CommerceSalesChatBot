import requests
import time

def test_cors_headers():
    # Wait for server to start
    time.sleep(3)
    
    base_url = 'http://localhost:5000'
    
    print("Testing CORS headers...")
    
    # Test OPTIONS request (preflight)
    print("1. Testing OPTIONS request:")
    options_response = requests.options(f'{base_url}/api/products')
    print(f'   Status: {options_response.status_code}')
    print(f'   CORS Headers:')
    for header, value in options_response.headers.items():
        if 'access-control' in header.lower():
            print(f'     {header}: {value}')
    
    # Test GET request
    print("\n2. Testing GET request:")
    get_response = requests.get(f'{base_url}/api/products?page=1&limit=5')
    print(f'   Status: {get_response.status_code}')
    print(f'   CORS Headers:')
    for header, value in get_response.headers.items():
        if 'access-control' in header.lower():
            print(f'     {header}: {value}')
    
    if get_response.status_code == 200:
        data = get_response.json()
        print(f'   Products returned: {len(data.get("products", []))}')
    else:
        print(f'   Error: {get_response.text[:200]}')

if __name__ == '__main__':
    test_cors_headers()
