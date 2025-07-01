import random

# Sample product data with real images
product_data = {
    'Electronics': [
        {
            'name': 'iPhone 15 Pro',
            'description': 'Latest flagship smartphone with A17 Pro chip, titanium design, and advanced camera system',
            'price': 999.99,
            'image_url': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=400&fit=crop',
            'stock': 50
        },
        {
            'name': 'MacBook Pro M3',
            'description': 'High-performance laptop with M3 chip, perfect for professionals and creators',
            'price': 1999.99,
            'image_url': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400&h=400&fit=crop',
            'stock': 30
        },
        {
            'name': 'Samsung Galaxy S24',
            'description': 'Premium Android smartphone with AI features and exceptional camera quality',
            'price': 899.99,
            'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop',
            'stock': 45
        },
        {
            'name': 'iPad Air',
            'description': 'Versatile tablet with M2 chip, perfect for work and entertainment',
            'price': 599.99,
            'image_url': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop',
            'stock': 60
        },
        {
            'name': 'AirPods Pro',
            'description': 'Premium wireless earbuds with active noise cancellation',
            'price': 249.99,
            'image_url': 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=400&h=400&fit=crop',
            'stock': 100
        },
        {
            'name': 'Apple Watch Series 9',
            'description': 'Advanced smartwatch with health monitoring and fitness tracking',
            'price': 399.99,
            'image_url': 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400&h=400&fit=crop',
            'stock': 75
        },
        {
            'name': 'Dell XPS 13',
            'description': 'Ultra-portable laptop with stunning InfinityEdge display',
            'price': 1299.99,
            'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop',
            'stock': 40
        },
        {
            'name': 'Sony WH-1000XM5',
            'description': 'Industry-leading noise canceling wireless headphones',
            'price': 399.99,
            'image_url': 'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=400&fit=crop',
            'stock': 80
        },
        {
            'name': 'Nintendo Switch OLED',
            'description': 'Portable gaming console with vibrant OLED screen',
            'price': 349.99,
            'image_url': 'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400&h=400&fit=crop',
            'stock': 65
        },
        {
            'name': 'LG 4K Monitor',
            'description': '27-inch 4K UHD monitor with HDR support',
            'price': 449.99,
            'image_url': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop',
            'stock': 35
        }
    ],
    'Books': [
        {
            'name': 'Clean Code',
            'description': 'A handbook of agile software craftsmanship by Robert C. Martin',
            'price': 42.99,
            'image_url': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=400&fit=crop',
            'stock': 100
        },
        {
            'name': 'JavaScript: The Good Parts',
            'description': 'Essential guide to JavaScript programming by Douglas Crockford',
            'price': 34.99,
            'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop',
            'stock': 85
        },
        {
            'name': 'The Pragmatic Programmer',
            'description': 'Your journey to mastery in software development',
            'price': 39.99,
            'image_url': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=400&fit=crop',
            'stock': 90
        },
        {
            'name': 'Design Patterns',
            'description': 'Elements of reusable object-oriented software',
            'price': 54.99,
            'image_url': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400&h=400&fit=crop',
            'stock': 70
        },
        {
            'name': 'You Don\'t Know JS',
            'description': 'Deep dive into the core mechanisms of JavaScript',
            'price': 29.99,
            'image_url': 'https://images.unsplash.com/photo-1551033406-611cf9a28f67?w=400&h=400&fit=crop',
            'stock': 110
        }
    ],
    'Clothing': [
        {
            'name': 'Premium Cotton T-Shirt',
            'description': 'Soft, comfortable cotton t-shirt in various colors',
            'price': 24.99,
            'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop',
            'stock': 200
        },
        {
            'name': 'Classic Denim Jeans',
            'description': 'Timeless denim jeans with perfect fit and comfort',
            'price': 79.99,
            'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop',
            'stock': 150
        },
        {
            'name': 'Wool Sweater',
            'description': 'Cozy wool sweater perfect for cold weather',
            'price': 89.99,
            'image_url': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=400&fit=crop',
            'stock': 80
        },
        {
            'name': 'Running Shoes',
            'description': 'Lightweight running shoes with excellent cushioning',
            'price': 129.99,
            'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop',
            'stock': 120
        },
        {
            'name': 'Leather Jacket',
            'description': 'Genuine leather jacket with classic styling',
            'price': 299.99,
            'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop',
            'stock': 45
        }
    ],
    'Home & Garden': [
        {
            'name': 'Smart LED Bulbs',
            'description': 'WiFi-enabled LED bulbs with color changing capabilities',
            'price': 39.99,
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop',
            'stock': 150
        },
        {
            'name': 'Coffee Maker',
            'description': 'Programmable coffee maker with thermal carafe',
            'price': 89.99,
            'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=400&fit=crop',
            'stock': 45
        },
        {
            'name': 'Indoor Plant Set',
            'description': 'Collection of easy-care indoor plants for home decoration',
            'price': 49.99,
            'image_url': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=400&fit=crop',
            'stock': 75
        },
        {
            'name': 'Aromatherapy Diffuser',
            'description': 'Ultrasonic essential oil diffuser with LED lights',
            'price': 34.99,
            'image_url': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop',
            'stock': 90
        },
        {
            'name': 'Kitchen Knife Set',
            'description': 'Professional-grade kitchen knives with wooden block',
            'price': 159.99,
            'image_url': 'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=400&h=400&fit=crop',
            'stock': 60
        }
    ],
    'Sports & Fitness': [
        {
            'name': 'Yoga Mat',
            'description': 'Non-slip yoga mat with excellent cushioning',
            'price': 29.99,
            'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=400&fit=crop',
            'stock': 120
        },
        {
            'name': 'Resistance Bands Set',
            'description': 'Complete set of resistance bands for home workouts',
            'price': 24.99,
            'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop',
            'stock': 100
        },
        {
            'name': 'Dumbbells Set',
            'description': 'Adjustable dumbbells for strength training',
            'price': 199.99,
            'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop',
            'stock': 40
        },
        {
            'name': 'Fitness Tracker',
            'description': 'Advanced fitness tracker with heart rate monitoring',
            'price': 149.99,
            'image_url': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400&h=400&fit=crop',
            'stock': 85
        },
        {
            'name': 'Protein Powder',
            'description': 'High-quality whey protein powder for muscle building',
            'price': 49.99,
            'image_url': 'https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&h=400&fit=crop',
            'stock': 200
        }
    ]
}

def generate_products(count=100):
    """Generate a list of products from the product data"""
    products = []
    
    for category, items in product_data.items():
        for item in items:
            product = {
                'name': item['name'],
                'description': item['description'],
                'price': item['price'],
                'category': category,
                'image_url': item['image_url'],
                'stock': item['stock'],
                'original_price': item['price'] + random.uniform(10, 50) if random.random() > 0.7 else None
            }
            products.append(product)
    
    # If we need more products, duplicate and modify existing ones
    while len(products) < count:
        base_product = random.choice(products)
        new_product = base_product.copy()
        new_product['name'] = f"{base_product['name']} - Variant {len(products)}"
        new_product['price'] = round(base_product['price'] * random.uniform(0.8, 1.2), 2)
        products.append(new_product)
    
    return products[:count]
