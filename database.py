#!/usr/bin/env python3
"""
Database utilities for SQLite management.
This module provides functions for database initialization, backup, and maintenance.
"""

import sqlite3
import os
import shutil
from datetime import datetime
from app import app
from extensions import db
from models import User, Category, Product, CartItem, Order, OrderItem

def init_database():
    """Initialize the database with all tables."""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if database file exists
            db_path = get_database_path()
            if os.path.exists(db_path):
                print(f"📁 Database file location: {db_path}")
                print(f"📊 Database file size: {get_file_size(db_path)}")
            
            return True
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            return False

def get_database_path():
    """Get the path to the SQLite database file."""
    database_url = app.config['SQLALCHEMY_DATABASE_URI']
    if database_url.startswith('sqlite:///'):
        db_path = database_url.replace('sqlite:///', '')
        # Check if it's a relative path and if the file exists in instance folder
        if not os.path.isabs(db_path) and not os.path.exists(db_path):
            instance_path = os.path.join('instance', db_path)
            if os.path.exists(instance_path):
                return instance_path
        return db_path
    return 'ecommerce.db'

def get_file_size(file_path):
    """Get human-readable file size."""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def backup_database():
    """Create a backup of the SQLite database."""
    try:
        db_path = get_database_path()
        if not os.path.exists(db_path):
            print("❌ Database file not found!")
            return False
        
        # Create backups directory if it doesn't exist
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"ecommerce_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copy database file
        shutil.copy2(db_path, backup_path)
        
        print(f"✅ Database backed up successfully!")
        print(f"📁 Backup location: {backup_path}")
        print(f"📊 Backup size: {get_file_size(backup_path)}")
        
        return backup_path
    except Exception as e:
        print(f"❌ Error backing up database: {e}")
        return False

def get_database_stats():
    """Get statistics about the database."""
    with app.app_context():
        try:
            stats = {
                'users': User.query.count(),
                'categories': Category.query.count(),
                'products': Product.query.count(),
                'cart_items': CartItem.query.count(),
                'orders': Order.query.count(),
                'order_items': OrderItem.query.count()
            }
            
            print("📊 Database Statistics:")
            print("-" * 30)
            for table, count in stats.items():
                print(f"{table.replace('_', ' ').title()}: {count}")
            
            # Get database file info
            db_path = get_database_path()
            if os.path.exists(db_path):
                print(f"\n📁 Database file: {db_path}")
                print(f"📊 File size: {get_file_size(db_path)}")
                print(f"🕒 Last modified: {datetime.fromtimestamp(os.path.getmtime(db_path))}")
            
            return stats
        except Exception as e:
            print(f"❌ Error getting database stats: {e}")
            return {}

def execute_raw_query(query, params=None):
    """Execute a raw SQL query on the SQLite database."""
    db_path = get_database_path()
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                return [dict(row) for row in results]
            else:
                conn.commit()
                return cursor.rowcount
    except Exception as e:
        print(f"❌ Error executing query: {e}")
        return None

def get_table_schema(table_name):
    """Get the schema for a specific table."""
    query = f"PRAGMA table_info({table_name})"
    return execute_raw_query(query)

def list_all_tables():
    """List all tables in the database."""
    query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    tables = execute_raw_query(query)
    return [table['name'] for table in tables] if tables else []

def vacuum_database():
    """Optimize the SQLite database by running VACUUM."""
    try:
        db_path = get_database_path()
        original_size = os.path.getsize(db_path)
        
        with sqlite3.connect(db_path) as conn:
            conn.execute('VACUUM')
        
        new_size = os.path.getsize(db_path)
        saved_space = original_size - new_size
        
        print("✅ Database optimized successfully!")
        print(f"📊 Original size: {get_file_size(original_size)}")
        print(f"📊 New size: {get_file_size(new_size)}")
        print(f"💾 Space saved: {get_file_size(saved_space)}")
        
        return True
    except Exception as e:
        print(f"❌ Error optimizing database: {e}")
        return False

def reset_database():
    """Reset the database by dropping all tables and recreating them."""
    with app.app_context():
        try:
            # Drop all tables
            db.drop_all()
            print("🗑️  All tables dropped")
            
            # Recreate tables
            db.create_all()
            print("✅ Database reset successfully!")
            
            return True
        except Exception as e:
            print(f"❌ Error resetting database: {e}")
            return False

def export_to_sql(output_file='database_export.sql'):
    """Export database to SQL file."""
    try:
        db_path = get_database_path()
        
        with sqlite3.connect(db_path) as conn:
            with open(output_file, 'w') as f:
                for line in conn.iterdump():
                    f.write(f"{line}\n")
        
        print(f"✅ Database exported to {output_file}")
        print(f"📊 Export size: {get_file_size(output_file)}")
        
        return True
    except Exception as e:
        print(f"❌ Error exporting database: {e}")
        return False

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python database.py <command>")
        print("Commands:")
        print("  init     - Initialize database")
        print("  stats    - Show database statistics")
        print("  backup   - Create database backup")
        print("  vacuum   - Optimize database")
        print("  reset    - Reset database (WARNING: deletes all data)")
        print("  export   - Export database to SQL file")
        print("  tables   - List all tables")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'init':
        init_database()
    elif command == 'stats':
        get_database_stats()
    elif command == 'backup':
        backup_database()
    elif command == 'vacuum':
        vacuum_database()
    elif command == 'reset':
        confirm = input("⚠️  This will delete ALL data. Are you sure? (yes/no): ")
        if confirm.lower() == 'yes':
            reset_database()
        else:
            print("Operation cancelled.")
    elif command == 'export':
        export_to_sql()
    elif command == 'tables':
        tables = list_all_tables()
        print("📋 Database Tables:")
        for table in tables:
            print(f"  - {table}")
    else:
        print(f"Unknown command: {command}")
