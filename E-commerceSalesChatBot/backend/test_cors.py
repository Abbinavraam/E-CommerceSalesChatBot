import requests
import time

def test_cors_fix():
    # Wait for server to start
    time.sleep(3)
    
    base_url = 'http://localhost:5000'
    
    # Test with the exact parameters the frontend is sending
    params = {
        'page': 1,
        'limit': 12,
        'category': 'Electronics',
        'sort': 'name',
        'search': '',
        'min_price': 0,
        'max_price': 1000
    }
    
    print("Testing API with frontend parameters...")
    response = requests.get(f'{base_url}/api/products', params=params)
    
    print(f'Status: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        print(f'Products returned: {len(data.get("products", []))}')
        print(f'Total products: {data.get("total", 0)}')
        print(f'Current page: {data.get("current_page", 0)}')
        print(f'Per page: {data.get("per_page", 0)}')
        
        # Show first few products
        products = data.get('products', [])
        if products:
            print('\nFirst few products:')
            for product in products[:3]:
                print(f'- {product["name"]}: ${product["price"]}')
    else:
        print(f'Error: {response.text}')
    
    # Test without category filter
    print(f'\n=== Testing without category filter ===')
    params_no_cat = {
        'page': 1,
        'limit': 5,
        'sort': 'price_asc'
    }
    
    response2 = requests.get(f'{base_url}/api/products', params=params_no_cat)
    print(f'Status: {response2.status_code}')
    
    if response2.status_code == 200:
        data2 = response2.json()
        print(f'Products returned: {len(data2.get("products", []))}')
        print(f'Total products: {data2.get("total", 0)}')

if __name__ == '__main__':
    test_cors_fix()
