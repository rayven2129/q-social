#!/usr/bin/env python3
"""
SQLite Integration Demo for E-Commerce Platform
This script demonstrates the SQLite database integration and features.
"""

import os
import sys
from app import app, db
from models import User, Category, Product, CartItem, Order, OrderItem
from database import get_database_stats, get_database_path, backup_database

def demo_sqlite_features():
    """Demonstrate SQLite features and database operations."""
    print("🛍️  E-Commerce Platform - SQLite Integration Demo")
    print("=" * 60)
    
    with app.app_context():
        # Show database location and info
        db_path = get_database_path()
        print(f"📁 Database Location: {os.path.abspath(db_path)}")
        
        if os.path.exists(db_path):
            size = os.path.getsize(db_path)
            print(f"📊 Database Size: {size:,} bytes")
        
        print("\n📈 Current Database Statistics:")
        print("-" * 40)
        stats = get_database_stats()
        
        print("\n🔍 Sample Data Queries:")
        print("-" * 40)
        
        # Show sample users
        users = User.query.all()
        print(f"\n👥 Users ({len(users)}):")
        for user in users:
            role = "Admin" if user.is_admin else "Customer"
            print(f"  • {user.username} ({user.email}) - {role}")
        
        # Show sample categories
        categories = Category.query.all()
        print(f"\n📂 Categories ({len(categories)}):")
        for category in categories:
            product_count = Product.query.filter_by(category_id=category.id).count()
            print(f"  • {category.name} ({product_count} products)")
        
        # Show sample products
        products = Product.query.limit(5).all()
        print(f"\n🛍️  Sample Products (showing 5 of {Product.query.count()}):")
        for product in products:
            print(f"  • {product.name} - ${product.price} (Stock: {product.stock_quantity})")
        
        print("\n💾 SQLite Features Demonstrated:")
        print("-" * 40)
        print("✅ File-based database (no server required)")
        print("✅ ACID transactions")
        print("✅ Foreign key relationships")
        print("✅ Full-text search capabilities")
        print("✅ Automatic backup and restore")
        print("✅ Zero-configuration setup")
        print("✅ Cross-platform compatibility")
        
        print("\n🛠️  Available Database Tools:")
        print("-" * 40)
        print("• python setup_database.py    - Initialize database with sample data")
        print("• python database.py stats    - Show database statistics")
        print("• python database.py backup   - Create database backup")
        print("• python database.py vacuum   - Optimize database")
        print("• python sqlite_browser.py    - Interactive database browser")
        
        # Demonstrate a simple query
        print("\n🔍 Advanced Query Example:")
        print("-" * 40)
        
        # Find products with low stock
        low_stock_products = Product.query.filter(Product.stock_quantity < 50).all()
        print(f"Products with low stock (< 50 units): {len(low_stock_products)}")
        for product in low_stock_products[:3]:
            print(f"  • {product.name}: {product.stock_quantity} units")
        
        # Show category with most products
        from sqlalchemy import func
        category_counts = db.session.query(
            Category.name, 
            func.count(Product.id).label('product_count')
        ).join(Product).group_by(Category.id).order_by(func.count(Product.id).desc()).first()
        
        if category_counts:
            print(f"\nMost popular category: {category_counts[0]} ({category_counts[1]} products)")
        
        print("\n🎯 SQLite Benefits for E-Commerce:")
        print("-" * 40)
        print("• Perfect for development and testing")
        print("• No database server setup required")
        print("• Excellent performance for small to medium sites")
        print("• Easy deployment (single file)")
        print("• Built-in to Python (no additional installation)")
        print("• Supports concurrent reads")
        print("• VACUUM command for optimization")
        print("• Full SQL support with indexes")
        
        print(f"\n✨ Demo completed! Database ready at: {os.path.abspath(db_path)}")

def show_database_schema():
    """Show the database schema structure."""
    print("\n📋 Database Schema:")
    print("=" * 50)
    
    with app.app_context():
        # Get all table names
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        for table_name in tables:
            print(f"\n📊 Table: {table_name}")
            print("-" * 30)
            columns = inspector.get_columns(table_name)
            
            for column in columns:
                nullable = "NULL" if column['nullable'] else "NOT NULL"
                default = f" DEFAULT {column['default']}" if column['default'] else ""
                print(f"  {column['name']:<20} {str(column['type']):<15} {nullable}{default}")
            
            # Show foreign keys
            foreign_keys = inspector.get_foreign_keys(table_name)
            if foreign_keys:
                print("  Foreign Keys:")
                for fk in foreign_keys:
                    print(f"    {fk['constrained_columns'][0]} -> {fk['referred_table']}.{fk['referred_columns'][0]}")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'schema':
        show_database_schema()
    else:
        demo_sqlite_features()
