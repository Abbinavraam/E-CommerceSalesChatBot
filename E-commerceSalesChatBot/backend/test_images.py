import requests
import time

def test_products_with_images():
    time.sleep(3)  # Wait for server to start
    
    base_url = 'http://localhost:5000'
    
    print("Testing products with images...")
    
    # Test products endpoint
    response = requests.get(f'{base_url}/api/products?page=1&limit=5')
    print(f'Status: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f'Products returned: {len(products)}')
        print(f'Total products: {data.get("total", 0)}')
        
        print('\nFirst few products with images:')
        for product in products[:3]:
            print(f'- {product["name"]}: ${product["price"]}')
            print(f'  Category: {product["category"]}')
            print(f'  Image: {product.get("image_url", "NO IMAGE")}')
            print()
    else:
        print(f'Error: {response.text}')

if __name__ == '__main__':
    test_products_with_images()
