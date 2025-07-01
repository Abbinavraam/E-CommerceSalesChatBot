import requests
import urllib.parse

def test_category_with_spaces():
    base_url = 'http://localhost:5000'
    
    # Test Home & Garden with URL encoding
    category = 'Home & Garden'
    encoded_category = urllib.parse.quote(category)
    
    print(f"Testing category: {category}")
    print(f"URL encoded: {encoded_category}")
    
    response = requests.get(f'{base_url}/api/products?category={encoded_category}&per_page=5')
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f'Found {len(products)} products (Total: {data.get("total", 0)})')
        
        for product in products:
            print(f'- {product["name"]}: ${product["price"]}')
    else:
        print(f'Error: {response.status_code} - {response.text}')
    
    # Test Sports & Fitness
    print(f"\n=== Sports & Fitness ===")
    category2 = 'Sports & Fitness'
    encoded_category2 = urllib.parse.quote(category2)
    
    response2 = requests.get(f'{base_url}/api/products?category={encoded_category2}&per_page=5')
    
    if response2.status_code == 200:
        data2 = response2.json()
        products2 = data2.get('products', [])
        print(f'Found {len(products2)} products (Total: {data2.get("total", 0)})')
        
        for product in products2:
            print(f'- {product["name"]}: ${product["price"]}')
    else:
        print(f'Error: {response2.status_code} - {response2.text}')

if __name__ == '__main__':
    test_category_with_spaces()
