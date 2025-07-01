import requests
import json

def test_products():
    base_url = 'http://localhost:5000'
    
    # Test products endpoint
    print("Testing products endpoint...")
    response = requests.get(f'{base_url}/api/products?per_page=5')
    print(f'Status: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        print(f'Total products: {data.get("total", 0)}')
        print(f'Products per page: {len(data.get("products", []))}')
        print('\nSample products:')
        for product in data.get('products', [])[:3]:
            print(f'- {product["name"]}: ${product["price"]} ({product["category"]})')
            print(f'  Image: {product["image_url"]}')
            print(f'  Stock: {product["stock"]}')
            print()
    else:
        print(f'Error: {response.text}')
    
    # Test categories
    print("\nTesting categories...")
    response = requests.get(f'{base_url}/api/products/categories')
    if response.status_code == 200:
        categories = response.json()
        print(f'Categories: {categories}')
    else:
        print(f'Error: {response.text}')

if __name__ == '__main__':
    test_products()
