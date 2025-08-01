#!/usr/bin/env python3
"""
Complete database setup script for the e-commerce platform.
This script initializes the SQLite database and populates it with sample data.
"""

import os
import sys
from datetime import datetime
from app import app
from extensions import db
from models import User, Category, Product, CartItem, Order, OrderItem
from werkzeug.security import generate_password_hash
from decimal import Decimal

def setup_database():
    """Complete database setup with initialization and sample data."""
    print("🚀 Starting database setup...")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Check if database already exists
            db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            db_exists = os.path.exists(db_path)
            
            if db_exists:
                print(f"📁 Existing database found: {db_path}")
                response = input("Do you want to reset the database? (y/n): ")
                if response.lower() == 'y':
                    print("🗑️  Dropping existing tables...")
                    db.drop_all()
                else:
                    print("✅ Using existing database")
                    return True
            
            # Create all tables
            print("🏗️  Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Create sample data
            print("\n📝 Creating sample data...")
            create_sample_data()
            
            # Display database info
            print("\n📊 Database Setup Complete!")
            print("=" * 50)
            print(f"📁 Database location: {os.path.abspath(db_path)}")
            print(f"📊 Database size: {get_file_size(db_path)}")
            
            # Display test accounts
            print("\n👤 Test Accounts Created:")
            print("  Admin: username='admin', password='admin123'")
            print("  User:  username='testuser', password='test123'")
            
            # Display statistics
            print("\n📈 Database Statistics:")
            print(f"  Users: {User.query.count()}")
            print(f"  Categories: {Category.query.count()}")
            print(f"  Products: {Product.query.count()}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error setting up database: {e}")
            return False

def create_sample_data():
    """Create sample users, categories, and products."""
    
    # Create admin user
    print("👤 Creating admin user...")
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            first_name='Admin',
            last_name='User',
            is_admin=True,
            address='123 Admin Street\nAdmin City, AC 12345',
            phone='(555) 123-4567'
        )
        db.session.add(admin_user)
    
    # Create test user
    print("👤 Creating test user...")
    test_user = User.query.filter_by(username='testuser').first()
    if not test_user:
        test_user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('test123'),
            first_name='Test',
            last_name='User',
            address='456 Test Avenue\nTest City, TC 67890',
            phone='(555) 987-6543'
        )
        db.session.add(test_user)
    
    # Create categories
    print("📂 Creating product categories...")
    categories_data = [
        {
            'name': 'Electronics',
            'description': 'Latest gadgets, computers, phones, and electronic devices'
        },
        {
            'name': 'Clothing & Fashion',
            'description': 'Trendy clothing, shoes, and fashion accessories for all ages'
        },
        {
            'name': 'Books & Media',
            'description': 'Books, magazines, audiobooks, and educational materials'
        },
        {
            'name': 'Home & Garden',
            'description': 'Home improvement, furniture, and gardening supplies'
        },
        {
            'name': 'Sports & Outdoors',
            'description': 'Sports equipment, outdoor gear, and fitness accessories'
        },
        {
            'name': 'Health & Beauty',
            'description': 'Health products, cosmetics, and personal care items'
        }
    ]
    
    for cat_data in categories_data:
        category = Category.query.filter_by(name=cat_data['name']).first()
        if not category:
            category = Category(**cat_data)
            db.session.add(category)
    
    db.session.commit()
    
    # Get category references
    electronics = Category.query.filter_by(name='Electronics').first()
    clothing = Category.query.filter_by(name='Clothing & Fashion').first()
    books = Category.query.filter_by(name='Books & Media').first()
    home_garden = Category.query.filter_by(name='Home & Garden').first()
    sports = Category.query.filter_by(name='Sports & Outdoors').first()
    health_beauty = Category.query.filter_by(name='Health & Beauty').first()
    
    # Create sample products
    print("🛍️  Creating sample products...")
    products_data = [
        # Electronics
        {
            'name': 'Wireless Bluetooth Headphones',
            'description': 'Premium wireless headphones with active noise cancellation, 30-hour battery life, and crystal-clear audio quality. Perfect for music lovers and professionals.',
            'price': Decimal('129.99'),
            'stock_quantity': 45,
            'category_id': electronics.id
        },
        {
            'name': 'Smartphone Protective Case',
            'description': 'Ultra-durable protective case with military-grade drop protection and wireless charging compatibility. Available in multiple colors.',
            'price': Decimal('24.99'),
            'stock_quantity': 150,
            'category_id': electronics.id
        },
        {
            'name': 'USB-C Fast Charging Cable',
            'description': 'High-speed USB-C charging cable with reinforced connectors. 6 feet long, supports fast charging and data transfer.',
            'price': Decimal('15.99'),
            'stock_quantity': 200,
            'category_id': electronics.id
        },
        {
            'name': 'Wireless Charging Pad',
            'description': 'Sleek wireless charging pad compatible with all Qi-enabled devices. LED indicator and overcharge protection included.',
            'price': Decimal('34.99'),
            'stock_quantity': 75,
            'category_id': electronics.id
        },
        
        # Clothing & Fashion
        {
            'name': 'Premium Cotton T-Shirt',
            'description': 'Soft, breathable 100% organic cotton t-shirt. Pre-shrunk and available in 8 different colors. Unisex sizing.',
            'price': Decimal('22.99'),
            'stock_quantity': 120,
            'category_id': clothing.id
        },
        {
            'name': 'Classic Denim Jeans',
            'description': 'Timeless straight-fit denim jeans made from premium cotton blend. Comfortable and durable for everyday wear.',
            'price': Decimal('59.99'),
            'stock_quantity': 80,
            'category_id': clothing.id
        },
        {
            'name': 'Winter Puffer Jacket',
            'description': 'Warm, lightweight puffer jacket with water-resistant coating. Down insulation keeps you warm in cold weather.',
            'price': Decimal('119.99'),
            'stock_quantity': 35,
            'category_id': clothing.id
        },
        {
            'name': 'Running Sneakers',
            'description': 'Comfortable running shoes with cushioned sole and breathable mesh upper. Perfect for jogging and casual wear.',
            'price': Decimal('89.99'),
            'stock_quantity': 60,
            'category_id': clothing.id
        },
        
        # Books & Media
        {
            'name': 'Python Programming Masterclass',
            'description': 'Comprehensive guide to Python programming covering basics to advanced topics. Includes practical projects and exercises.',
            'price': Decimal('39.99'),
            'stock_quantity': 50,
            'category_id': books.id
        },
        {
            'name': 'Web Development Complete Guide',
            'description': 'Learn modern web development with HTML5, CSS3, JavaScript, and popular frameworks. Perfect for beginners and professionals.',
            'price': Decimal('44.99'),
            'stock_quantity': 40,
            'category_id': books.id
        },
        {
            'name': 'Digital Marketing Handbook',
            'description': 'Master digital marketing strategies including SEO, social media, content marketing, and analytics.',
            'price': Decimal('32.99'),
            'stock_quantity': 30,
            'category_id': books.id
        },
        
        # Home & Garden
        {
            'name': 'LED Desk Lamp with USB Charging',
            'description': 'Adjustable LED desk lamp with multiple brightness levels, color temperature control, and built-in USB charging port.',
            'price': Decimal('49.99'),
            'stock_quantity': 85,
            'category_id': home_garden.id
        },
        {
            'name': 'Ceramic Plant Pot Set',
            'description': 'Beautiful set of 3 ceramic plant pots with drainage holes and saucers. Perfect for indoor plants and herbs.',
            'price': Decimal('34.99'),
            'stock_quantity': 65,
            'category_id': home_garden.id
        },
        {
            'name': 'Smart Home Security Camera',
            'description': '1080p HD security camera with night vision, motion detection, and smartphone app control. Easy wireless setup.',
            'price': Decimal('79.99'),
            'stock_quantity': 25,
            'category_id': home_garden.id
        },
        
        # Sports & Outdoors
        {
            'name': 'Premium Yoga Mat',
            'description': 'Non-slip yoga mat with extra cushioning and alignment guides. Made from eco-friendly materials.',
            'price': Decimal('29.99'),
            'stock_quantity': 100,
            'category_id': sports.id
        },
        {
            'name': 'Insulated Water Bottle',
            'description': 'Stainless steel vacuum-insulated water bottle. Keeps drinks cold for 24 hours or hot for 12 hours.',
            'price': Decimal('24.99'),
            'stock_quantity': 150,
            'category_id': sports.id
        },
        {
            'name': 'Resistance Bands Set',
            'description': 'Complete set of resistance bands with different resistance levels, handles, and door anchor for full-body workouts.',
            'price': Decimal('19.99'),
            'stock_quantity': 90,
            'category_id': sports.id
        },
        
        # Health & Beauty
        {
            'name': 'Vitamin C Serum',
            'description': 'Anti-aging vitamin C serum with hyaluronic acid. Brightens skin and reduces fine lines.',
            'price': Decimal('27.99'),
            'stock_quantity': 70,
            'category_id': health_beauty.id
        },
        {
            'name': 'Electric Toothbrush',
            'description': 'Rechargeable electric toothbrush with multiple cleaning modes and 2-minute timer. Includes 2 brush heads.',
            'price': Decimal('69.99'),
            'stock_quantity': 40,
            'category_id': health_beauty.id
        }
    ]
    
    for product_data in products_data:
        product = Product.query.filter_by(name=product_data['name']).first()
        if not product:
            product = Product(**product_data)
            db.session.add(product)
    
    db.session.commit()
    print(f"✅ Created {len(categories_data)} categories and {len(products_data)} products")

def get_file_size(file_path):
    """Get human-readable file size."""
    if not os.path.exists(file_path):
        return "0 B"
    
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

if __name__ == '__main__':
    print("🛍️  E-Commerce Platform Database Setup")
    print("=" * 50)
    
    # Check if Flask app can be imported
    try:
        from app import app
        setup_database()
        print("\n🎉 Database setup completed successfully!")
        print("\nYou can now run the application with: python app.py")
    except ImportError as e:
        print(f"❌ Error importing Flask app: {e}")
        print("Make sure you're in the correct directory and all dependencies are installed.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
