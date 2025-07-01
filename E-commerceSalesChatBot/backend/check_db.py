from app import create_app, db
from app.models import Product

def check_database():
    app = create_app()
    
    with app.app_context():
        # Get all distinct categories
        categories = db.session.query(Product.category).distinct().all()
        print("Categories in database:")
        for cat in categories:
            print(f'- "{cat[0]}"')
        
        print(f"\nTotal products: {Product.query.count()}")
        
        # Count products per category
        print("\nProducts per category:")
        for cat in categories:
            count = Product.query.filter(Product.category == cat[0]).count()
            print(f'- {cat[0]}: {count} products')

if __name__ == '__main__':
    check_database()
