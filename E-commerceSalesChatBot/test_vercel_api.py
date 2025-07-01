#!/usr/bin/env python3
"""
Test script to verify the Vercel API endpoints work correctly
"""

import requests
import json
import sys

def test_api_endpoint(url, endpoint, method='GET', data=None):
    """Test a single API endpoint"""
    full_url = f"{url}{endpoint}"
    print(f"\n🧪 Testing {method} {endpoint}")
    
    try:
        if method == 'GET':
            response = requests.get(full_url)
        elif method == 'POST':
            response = requests.post(full_url, json=data, headers={'Content-Type': 'application/json'})
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                json_data = response.json()
                if endpoint == '/api/products':
                    print(f"   Products returned: {len(json_data.get('products', []))}")
                elif endpoint == '/api/products/categories':
                    print(f"   Categories: {json_data}")
                elif 'auth' in endpoint:
                    print(f"   Auth response: {json_data.get('message', 'No message')}")
                elif 'chat' in endpoint:
                    print(f"   Chat response: {json_data.get('message', 'No message')}")
                else:
                    print(f"   Response: {json_data}")
                print("   ✅ Success")
            except json.JSONDecodeError:
                print(f"   Response text: {response.text[:100]}...")
                print("   ✅ Success (non-JSON response)")
        else:
            print(f"   Error: {response.text}")
            print("   ❌ Failed")
            
    except requests.exceptions.RequestException as e:
        print(f"   Connection error: {e}")
        print("   ❌ Failed")

def main():
    # Test with local server first, then Vercel URL
    base_urls = [
        "http://localhost:5000",  # Local development
        # Add your Vercel URL here when deployed
        # "https://your-app.vercel.app"
    ]
    
    endpoints_to_test = [
        ('/', 'GET'),
        ('/api/products', 'GET'),
        ('/api/products/categories', 'GET'),
        ('/api/auth/login', 'POST', {'email': 'test@example.com', 'password': 'password123'}),
        ('/api/auth/register', 'POST', {'name': 'Test User', 'email': 'test@example.com', 'password': 'password123'}),
        ('/api/chat/start', 'POST', {}),
        ('/api/chat/message', 'POST', {'content': 'Hello', 'session_id': 'test-session'})
    ]
    
    for base_url in base_urls:
        print(f"\n🌐 Testing API at: {base_url}")
        print("=" * 50)
        
        for endpoint_data in endpoints_to_test:
            if len(endpoint_data) == 2:
                endpoint, method = endpoint_data
                data = None
            else:
                endpoint, method, data = endpoint_data
            
            test_api_endpoint(base_url, endpoint, method, data)
        
        print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
