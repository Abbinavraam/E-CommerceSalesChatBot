import requests

def test_categories():
    base_url = 'http://localhost:5000'
    
    categories = ['Electronics', 'Books', 'Clothing', 'Home & Garden', 'Sports & Fitness']
    
    for category in categories:
        print(f"\n=== {category} ===")
        response = requests.get(f'{base_url}/api/products?category={category}&per_page=5')
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f'Found {len(products)} products (Total in category: {data.get("total", 0)})')
            
            for product in products:
                print(f'- {product["name"]}: ${product["price"]}')
        else:
            print(f'Error: {response.text}')

if __name__ == '__main__':
    test_categories()
