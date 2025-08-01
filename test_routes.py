#!/usr/bin/env python3
"""
Test all routes to ensure they work properly.
"""

from app import app
from extensions import db
from models import User, Category, Product

def test_all_routes():
    """Test all application routes."""
    with app.test_client() as client:
        with app.app_context():
            print("🧪 Testing all application routes...")
            
            # Test home page
            response = client.get('/')
            print(f"Home page: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
            
            # Test products page
            response = client.get('/products')
            print(f"Products page: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
            
            # Test category filtering
            categories = Category.query.all()
            if categories:
                for category in categories[:3]:  # Test first 3 categories
                    response = client.get(f'/products?category={category.id}')
                    print(f"Category {category.name}: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
            
            # Test product detail
            products = Product.query.limit(3).all()
            if products:
                for product in products:
                    response = client.get(f'/product/{product.id}')
                    print(f"Product {product.name}: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
            
            # Test login page
            response = client.get('/login')
            print(f"Login page: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
            
            # Test register page
            response = client.get('/register')
            print(f"Register page: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
            
            # Test search
            response = client.get('/products?search=headphones')
            print(f"Search functionality: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
            
            print("\n📊 Route testing completed!")

if __name__ == '__main__':
    test_all_routes()
