import requests

def test_frontend_requests():
    base_url = 'http://localhost:5000'
    
    # Test the exact requests that the frontend is making
    test_requests = [
        {
            'name': 'Initial load',
            'url': f'{base_url}/api/products?page=1&limit=12&category=&sort=name&search=&min_price=0&max_price=1000'
        },
        {
            'name': 'Electronics filter',
            'url': f'{base_url}/api/products?page=1&limit=12&category=Electronics&sort=name&search=&min_price=0&max_price=1000'
        },
        {
            'name': 'Sports & Fitness filter',
            'url': f'{base_url}/api/products?page=1&limit=12&category=Sports+%26+Fitness&sort=name&search=&min_price=444&max_price=536'
        }
    ]
    
    for test in test_requests:
        print(f"\nTesting: {test['name']}")
        print(f"URL: {test['url']}")
        
        try:
            response = requests.get(test['url'])
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                products = data.get('products', [])
                print(f"Products returned: {len(products)}")
                print(f"Total available: {data.get('total', 0)}")
                
                if products:
                    print(f"First product: {products[0]['name']} - ${products[0]['price']}")
            else:
                print(f"Error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"Exception: {str(e)}")

if __name__ == '__main__':
    test_frontend_requests()
