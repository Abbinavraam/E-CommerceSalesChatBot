from app import create_app, db
from app.models import Product
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
            'name': 'Sony WH-1000XM5',
            'description': 'Industry-leading noise canceling wireless headphones',
            'price': 399.99,
            'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
            'stock': 40
        },
        {
            'name': 'Nintendo Switch OLED',
            'description': 'Portable gaming console with vibrant OLED display',
            'price': 349.99,
            'image_url': 'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400&h=400&fit=crop',
            'stock': 35
        },
        {
            'name': 'Dell XPS 13',
            'description': 'Ultra-portable laptop with stunning InfinityEdge display',
            'price': 1299.99,
            'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop',
            'stock': 25
        },
        {
            'name': 'Samsung 4K Monitor',
            'description': '27-inch 4K UHD monitor with HDR support for professionals',
            'price': 449.99,
            'image_url': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop',
            'stock': 20
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
            'description': 'Essential guide to JavaScript programming best practices',
            'price': 34.99,
            'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop',
            'stock': 85
        },
        {
            'name': 'Design Patterns',
            'description': 'Elements of reusable object-oriented software',
            'price': 54.99,
            'image_url': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=400&fit=crop',
            'stock': 60
        },
        {
            'name': 'The Pragmatic Programmer',
            'description': 'Your journey to mastery in software development',
            'price': 45.99,
            'image_url': 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=400&fit=crop',
            'stock': 75
        },
        {
            'name': 'Atomic Habits',
            'description': 'An easy & proven way to build good habits & break bad ones',
            'price': 18.99,
            'image_url': 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400&h=400&fit=crop',
            'stock': 120
        },
        {
            'name': 'Sapiens',
            'description': 'A brief history of humankind by Yuval Noah Harari',
            'price': 16.99,
            'image_url': 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400&h=400&fit=crop',
            'stock': 90
        },
        {
            'name': 'The Psychology of Money',
            'description': 'Timeless lessons on wealth, greed, and happiness',
            'price': 22.99,
            'image_url': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=400&h=400&fit=crop',
            'stock': 110
        },
        {
            'name': 'Thinking, Fast and Slow',
            'description': 'Insights into how the mind makes decisions',
            'price': 19.99,
            'image_url': 'https://images.unsplash.com/photo-1592496431122-2349e0fbc666?w=400&h=400&fit=crop',
            'stock': 80
        },
        {
            'name': 'The Lean Startup',
            'description': 'How todays entrepreneurs use continuous innovation',
            'price': 28.99,
            'image_url': 'https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=400&h=400&fit=crop',
            'stock': 65
        },
        {
            'name': 'You Don\'t Know JS',
            'description': 'Deep dive into the core mechanisms of JavaScript',
            'price': 39.99,
            'image_url': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400&h=400&fit=crop',
            'stock': 70
        }
    ],
    'Clothing': [
        {
            'name': 'Premium Cotton T-Shirt',
            'description': 'Soft, breathable cotton t-shirt perfect for everyday wear',
            'price': 24.99,
            'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop',
            'stock': 200
        },
        {
            'name': 'Classic Denim Jeans',
            'description': 'Timeless straight-fit jeans made from premium denim',
            'price': 79.99,
            'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop',
            'stock': 150
        },
        {
            'name': 'Wool Sweater',
            'description': 'Cozy merino wool sweater for cold weather',
            'price': 89.99,
            'image_url': 'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=400&fit=crop',
            'stock': 80
        },
        {
            'name': 'Leather Jacket',
            'description': 'Genuine leather jacket with classic biker style',
            'price': 299.99,
            'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop',
            'stock': 25
        },
        {
            'name': 'Summer Dress',
            'description': 'Elegant floral dress perfect for summer occasions',
            'price': 69.99,
            'image_url': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop',
            'stock': 60
        },
        {
            'name': 'Running Shoes',
            'description': 'Lightweight athletic shoes with superior cushioning',
            'price': 129.99,
            'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop',
            'stock': 90
        },
        {
            'name': 'Business Shirt',
            'description': 'Professional dress shirt for office and formal occasions',
            'price': 49.99,
            'image_url': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&h=400&fit=crop',
            'stock': 120
        },
        {
            'name': 'Casual Sneakers',
            'description': 'Comfortable everyday sneakers with modern design',
            'price': 89.99,
            'image_url': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop',
            'stock': 110
        }
    ],
    'Home & Garden': [
        {
            'name': 'Smart LED Bulbs',
            'description': 'WiFi-enabled color-changing LED bulbs with app control',
            'price': 39.99,
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop',
            'stock': 150
        },
        {
            'name': 'Coffee Maker',
            'description': 'Programmable drip coffee maker with thermal carafe',
            'price': 89.99,
            'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=400&fit=crop',
            'stock': 45
        },
        {
            'name': 'Indoor Plant Set',
            'description': 'Collection of low-maintenance houseplants with decorative pots',
            'price': 59.99,
            'image_url': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=400&fit=crop',
            'stock': 75
        },
        {
            'name': 'Throw Pillows',
            'description': 'Set of decorative throw pillows in modern patterns',
            'price': 34.99,
            'image_url': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=400&fit=crop',
            'stock': 100
        },
        {
            'name': 'Essential Oil Diffuser',
            'description': 'Ultrasonic aromatherapy diffuser with LED lighting',
            'price': 49.99,
            'image_url': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop',
            'stock': 80
        }
    ],
    'Sports & Fitness': [
        {
            'name': 'Yoga Mat',
            'description': 'Non-slip premium yoga mat with carrying strap',
            'price': 29.99,
            'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=400&fit=crop',
            'stock': 120
        },
        {
            'name': 'Resistance Bands Set',
            'description': 'Complete set of resistance bands for home workouts',
            'price': 24.99,
            'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop',
            'stock': 90
        },
        {
            'name': 'Dumbbell Set',
            'description': 'Adjustable dumbbells for strength training',
            'price': 199.99,
            'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop',
            'stock': 30
        },
        {
            'name': 'Fitness Tracker',
            'description': 'Waterproof fitness tracker with heart rate monitoring',
            'price': 79.99,
            'image_url': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400&h=400&fit=crop',
            'stock': 65
        },
        {
            'name': 'Protein Powder',
            'description': 'Whey protein powder for muscle building and recovery',
            'price': 39.99,
            'image_url': 'https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&h=400&fit=crop',
            'stock': 85
        }
    ]
}

def generate_products(num_products=300):
    """Generate a specified number of mock products"""
    products = []
    categories = list(product_data.keys())

    # First, add all base products as-is
    for category, category_products in product_data.items():
        for product in category_products:
            base_product = {
                'name': product['name'],
                'description': product['description'],
                'price': product['price'],
                'category': category,
                'stock': product['stock'],
                'image_url': product['image_url']
            }
            products.append(base_product)

    # Then generate variations to reach the target number
    remaining_products = num_products - len(products)

    for _ in range(remaining_products):
        # Select random category and base product
        category = random.choice(categories)
        base_product = random.choice(product_data[category])

        # Create variation of base product with different attributes
        variation_types = ['Pro', 'Plus', 'Lite', 'Max', 'Mini', 'Deluxe', 'Premium', 'Standard', 'Advanced', 'Basic']
        colors = ['Black', 'White', 'Blue', 'Red', 'Green', 'Gray', 'Silver', 'Gold', 'Rose Gold', 'Navy']
        sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL'] if category == 'Clothing' else ['Small', 'Medium', 'Large']

        # Choose variation strategy
        variation_strategy = random.choice(['type', 'color', 'size', 'model'])

        if variation_strategy == 'type':
            variation_name = f"{base_product['name']} {random.choice(variation_types)}"
        elif variation_strategy == 'color':
            variation_name = f"{random.choice(colors)} {base_product['name']}"
        elif variation_strategy == 'size':
            variation_name = f"{base_product['name']} ({random.choice(sizes)})"
        else:
            variation_name = f"{base_product['name']} Model {random.randint(100, 999)}"

        variation = {
            'name': variation_name,
            'description': base_product['description'],
            'price': round(base_product['price'] * random.uniform(0.7, 1.3), 2),
            'category': category,
            'stock': random.randint(0, 250),
            'image_url': base_product['image_url']
        }

        products.append(variation)

    return products

def populate_database():
    """Populate the database with mock products"""
    app = create_app()
    
    with app.app_context():
        # Clear existing products
        Product.query.delete()
        
        # Generate and add new products
        products = generate_products()
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        print(f"Added {len(products)} products to the database.")

if __name__ == '__main__':
    populate_database()