#!/usr/bin/env python3
"""
Sample data script to populate the e-commerce database with test data.
Run this script after setting up the database to add sample products and categories.
"""

from app import app, db
from models import User, Category, Product
from werkzeug.security import generate_password_hash
from decimal import Decimal

def create_sample_data():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create admin user
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                first_name='Admin',
                last_name='User',
                is_admin=True
            )
            db.session.add(admin_user)
        
        # Create test user
        test_user = User.query.filter_by(username='testuser').first()
        if not test_user:
            test_user = User(
                username='testuser',
                email='test@example.com',
                password_hash=generate_password_hash('test123'),
                first_name='Test',
                last_name='User',
                address='123 Test Street\nTest City, TC 12345'
            )
            db.session.add(test_user)
        
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Computers, phones, and electronic devices'},
            {'name': 'Clothing', 'description': 'Fashion and apparel for all ages'},
            {'name': 'Books', 'description': 'Books, magazines, and educational materials'},
            {'name': 'Home & Garden', 'description': 'Home improvement and gardening supplies'},
            {'name': 'Sports', 'description': 'Sports equipment and outdoor gear'},
        ]
        
        for cat_data in categories_data:
            category = Category.query.filter_by(name=cat_data['name']).first()
            if not category:
                category = Category(**cat_data)
                db.session.add(category)
        
        db.session.commit()
        
        # Create sample products
        electronics = Category.query.filter_by(name='Electronics').first()
        clothing = Category.query.filter_by(name='Clothing').first()
        books = Category.query.filter_by(name='Books').first()
        home_garden = Category.query.filter_by(name='Home & Garden').first()
        sports = Category.query.filter_by(name='Sports').first()
        
        products_data = [
            # Electronics
            {
                'name': 'Wireless Bluetooth Headphones',
                'description': 'High-quality wireless headphones with noise cancellation and 30-hour battery life.',
                'price': Decimal('99.99'),
                'stock_quantity': 50,
                'category_id': electronics.id
            },
            {
                'name': 'Smartphone Case',
                'description': 'Durable protective case for smartphones with shock absorption.',
                'price': Decimal('24.99'),
                'stock_quantity': 100,
                'category_id': electronics.id
            },
            {
                'name': 'USB-C Charging Cable',
                'description': 'Fast charging USB-C cable, 6 feet long, compatible with most devices.',
                'price': Decimal('12.99'),
                'stock_quantity': 200,
                'category_id': electronics.id
            },
            
            # Clothing
            {
                'name': 'Cotton T-Shirt',
                'description': 'Comfortable 100% cotton t-shirt available in multiple colors and sizes.',
                'price': Decimal('19.99'),
                'stock_quantity': 75,
                'category_id': clothing.id
            },
            {
                'name': 'Denim Jeans',
                'description': 'Classic fit denim jeans made from premium cotton blend.',
                'price': Decimal('49.99'),
                'stock_quantity': 40,
                'category_id': clothing.id
            },
            {
                'name': 'Winter Jacket',
                'description': 'Warm and waterproof winter jacket with insulated lining.',
                'price': Decimal('89.99'),
                'stock_quantity': 25,
                'category_id': clothing.id
            },
            
            # Books
            {
                'name': 'Python Programming Guide',
                'description': 'Comprehensive guide to Python programming for beginners and advanced users.',
                'price': Decimal('34.99'),
                'stock_quantity': 30,
                'category_id': books.id
            },
            {
                'name': 'Web Development Handbook',
                'description': 'Complete handbook covering HTML, CSS, JavaScript, and modern frameworks.',
                'price': Decimal('42.99'),
                'stock_quantity': 20,
                'category_id': books.id
            },
            
            # Home & Garden
            {
                'name': 'LED Desk Lamp',
                'description': 'Adjustable LED desk lamp with multiple brightness levels and USB charging port.',
                'price': Decimal('39.99'),
                'stock_quantity': 60,
                'category_id': home_garden.id
            },
            {
                'name': 'Plant Pot Set',
                'description': 'Set of 3 ceramic plant pots with drainage holes, perfect for indoor plants.',
                'price': Decimal('29.99'),
                'stock_quantity': 45,
                'category_id': home_garden.id
            },
            
            # Sports
            {
                'name': 'Yoga Mat',
                'description': 'Non-slip yoga mat with extra cushioning, perfect for yoga and exercise.',
                'price': Decimal('24.99'),
                'stock_quantity': 80,
                'category_id': sports.id
            },
            {
                'name': 'Water Bottle',
                'description': 'Stainless steel insulated water bottle, keeps drinks cold for 24 hours.',
                'price': Decimal('19.99'),
                'stock_quantity': 120,
                'category_id': sports.id
            },
        ]
        
        for product_data in products_data:
            product = Product.query.filter_by(name=product_data['name']).first()
            if not product:
                product = Product(**product_data)
                db.session.add(product)
        
        db.session.commit()
        print("Sample data created successfully!")
        print("\nTest accounts created:")
        print("Admin: username='admin', password='admin123'")
        print("User: username='testuser', password='test123'")
        print(f"\nCreated {len(categories_data)} categories and {len(products_data)} products.")

if __name__ == '__main__':
    create_sample_data()
