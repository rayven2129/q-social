# SQLite Integration Guide

## Overview

This e-commerce platform is fully integrated with SQLite, providing a robust, file-based database solution that requires zero configuration and works perfectly for development, testing, and small to medium-scale production deployments.

## 🗄️ Database Features

### Core SQLite Benefits
- **Zero Configuration**: No database server setup required
- **File-Based**: Single file database (`ecommerce.db`)
- **ACID Compliant**: Reliable transactions and data integrity
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Built-in to Python**: No additional database software needed
- **Concurrent Reads**: Multiple users can read simultaneously
- **Full SQL Support**: Complete SQL functionality with indexes

### Database Schema
```
📊 Tables:
├── user (User accounts and authentication)
├── category (Product categories)
├── product (Product catalog with inventory)
├── cart_item (Shopping cart items)
├── order (Customer orders)
└── order_item (Individual items within orders)
```

## 🚀 Quick Start

### 1. Setup Database
```bash
# Complete setup with sample data
python setup_database.py

# Alternative: Use original sample data script
python sample_data.py
```

### 2. Run Application
```bash
python app.py
```

The database file will be created at `instance/ecommerce.db`

## 🛠️ Database Management Tools

### Database Utilities (`database.py`)
```bash
# Show database statistics
python database.py stats

# Create database backup
python database.py backup

# Optimize database (VACUUM)
python database.py vacuum

# Export database to SQL file
python database.py export

# Reset database (WARNING: deletes all data)
python database.py reset

# List all tables
python database.py tables
```

### SQLite Browser (`sqlite_browser.py`)
Interactive command-line database browser:

```bash
# Start interactive mode
python sqlite_browser.py

# Quick commands
python sqlite_browser.py tables              # List all tables
python sqlite_browser.py info                # Database information
python sqlite_browser.py schema users        # Show table schema
python sqlite_browser.py browse products 20  # Browse products (limit 20)
python sqlite_browser.py query "SELECT * FROM user"  # Custom query
```

### Demo Script (`demo_sqlite.py`)
```bash
# Run SQLite integration demo
python demo_sqlite.py

# Show database schema
python demo_sqlite.py schema
```

## 📁 Database Configuration

### Environment Variables
```bash
# Default SQLite configuration
DATABASE_URL=sqlite:///ecommerce.db

# For production, consider PostgreSQL or MySQL:
# DATABASE_URL=postgresql://username:password@localhost/ecommerce
# DATABASE_URL=mysql://username:password@localhost/ecommerce
```

### Flask Configuration
```python
# SQLite-specific optimizations
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
```

## 🔍 Database Operations

### Sample Queries
```python
# Get all products with low stock
low_stock = Product.query.filter(Product.stock_quantity < 50).all()

# Find products by category
electronics = Product.query.join(Category).filter(Category.name == 'Electronics').all()

# Get user's order history
user_orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()

# Calculate total sales
from sqlalchemy import func
total_sales = db.session.query(func.sum(Order.total_amount)).scalar()
```

### Advanced Features
```python
# Full-text search (if FTS is enabled)
products = Product.query.filter(Product.name.contains(search_term)).all()

# Aggregate queries
category_stats = db.session.query(
    Category.name,
    func.count(Product.id).label('product_count'),
    func.avg(Product.price).label('avg_price')
).join(Product).group_by(Category.id).all()
```

## 💾 Backup and Maintenance

### Automatic Backups
```python
from database import backup_database

# Create timestamped backup
backup_path = backup_database()
print(f"Backup created: {backup_path}")
```

### Database Optimization
```bash
# Optimize database file size
python database.py vacuum

# This reclaims unused space and optimizes the database
```

### Monitoring
```python
# Check database size and statistics
from database import get_database_stats, get_file_size
import os

stats = get_database_stats()
db_path = 'instance/ecommerce.db'
size = get_file_size(db_path)
print(f"Database size: {size}")
```

## 🔧 Production Considerations

### Performance Optimization
1. **Indexes**: Automatically created for foreign keys and primary keys
2. **VACUUM**: Regular optimization to reclaim space
3. **WAL Mode**: Consider enabling for better concurrency
4. **Connection Pooling**: Configured in Flask-SQLAlchemy

### Scaling Options
```python
# For larger applications, consider upgrading to PostgreSQL:
# pip install psycopg2-binary
# DATABASE_URL=postgresql://user:pass@localhost/ecommerce

# Or MySQL:
# pip install PyMySQL
# DATABASE_URL=mysql+pymysql://user:pass@localhost/ecommerce
```

### Security
- Database file permissions should be restricted
- Regular backups to secure location
- Consider encryption for sensitive data
- Use parameterized queries (automatically handled by SQLAlchemy)

## 📊 Database Schema Details

### User Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(120) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_admin BOOLEAN DEFAULT FALSE
);
```

### Product Table
```sql
CREATE TABLE product (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    image_filename VARCHAR(100),
    category_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (category_id) REFERENCES category(id)
);
```

### Order Table
```sql
CREATE TABLE "order" (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    payment_intent_id VARCHAR(100),
    shipping_address TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

## 🎯 Best Practices

### Development
1. Use `setup_database.py` for consistent database initialization
2. Regular backups during development
3. Use the SQLite browser for debugging
4. Monitor database size and performance

### Testing
```python
# Use in-memory database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
```

### Deployment
1. Ensure database file has proper permissions
2. Set up automated backups
3. Monitor database size and performance
4. Consider read replicas for high-traffic sites

## 🔗 Integration Examples

### Flask Route with Database
```python
@app.route('/products')
def products():
    category_id = request.args.get('category')
    search = request.args.get('search')
    
    query = Product.query.filter_by(is_active=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(Product.name.contains(search))
    
    products = query.all()
    return render_template('products.html', products=products)
```

### Transaction Example
```python
from app import db

try:
    # Start transaction
    db.session.begin()
    
    # Create order
    order = Order(user_id=user.id, total_amount=total)
    db.session.add(order)
    db.session.flush()  # Get order ID
    
    # Add order items
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        db.session.add(order_item)
        
        # Update stock
        cart_item.product.stock_quantity -= cart_item.quantity
    
    # Clear cart
    CartItem.query.filter_by(user_id=user.id).delete()
    
    # Commit transaction
    db.session.commit()
    
except Exception as e:
    db.session.rollback()
    raise e
```

## 📈 Monitoring and Analytics

### Database Statistics
```python
def get_analytics():
    with app.app_context():
        return {
            'total_users': User.query.count(),
            'total_products': Product.query.count(),
            'total_orders': Order.query.count(),
            'total_revenue': db.session.query(func.sum(Order.total_amount)).scalar() or 0,
            'active_products': Product.query.filter_by(is_active=True).count(),
            'low_stock_products': Product.query.filter(Product.stock_quantity < 10).count()
        }
```

This comprehensive SQLite integration provides a solid foundation for your e-commerce platform with excellent development experience and production-ready features.
