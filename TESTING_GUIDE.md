# 🧪 Testing & Running Guide

## 🚀 Quick Start (Step-by-Step)

### 1. **Environment Setup**
```bash
# Navigate to project directory
cd q-social

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. **Configuration**
```bash
# Copy environment template
cp .env.example .env

# Edit .env file (optional for testing)
# The default values work for development
```

### 3. **Database Setup**
```bash
# Initialize database with sample data
python setup_database.py
```

### 4. **Run Application**
```bash
# Start the Flask development server
python app.py
```

**Application will be available at:** `http://localhost:5000`

---

## 👤 Test Accounts

After running `setup_database.py`, you'll have these accounts:

| Role | Username | Password | Description |
|------|----------|----------|-------------|
| **Admin** | `admin` | `admin123` | Full admin access |
| **Customer** | `testuser` | `test123` | Regular customer account |

---

## 🧪 Testing Features

### **1. User Authentication**
- **Register**: Create new account at `/register`
- **Login**: Sign in at `/login`
- **Logout**: Sign out (available when logged in)

### **2. Product Catalog**
- **Browse Products**: Visit `/products`
- **Search**: Use search bar to find products
- **Filter by Category**: Click category filters
- **Product Details**: Click on any product

### **3. Shopping Cart**
- **Add to Cart**: Click "Add to Cart" on product pages
- **View Cart**: Click cart icon in navigation
- **Update Quantities**: Change quantities in cart
- **Remove Items**: Remove items from cart

### **4. Order Management**
- **Checkout**: Proceed from cart to checkout
- **View Orders**: See order history at `/orders`
- **Order Details**: Click on any order to see details

### **5. Admin Features**
- **Admin Dashboard**: Login as admin, visit `/admin`
- **View Statistics**: See user, product, and order counts
- **Manage Data**: Basic overview of products and orders

---

## 🔧 Database Testing

### **Database Utilities**
```bash
# Show database statistics
python database.py stats

# Create database backup
python database.py backup

# List all tables
python database.py tables

# Optimize database
python database.py vacuum

# Reset database (WARNING: deletes all data)
python database.py reset
```

### **SQLite Browser**
```bash
# Interactive database browser
python sqlite_browser.py

# Quick commands
python sqlite_browser.py tables
python sqlite_browser.py info
python sqlite_browser.py browse products 10
python sqlite_browser.py schema users
```

### **Demo Script**
```bash
# Run SQLite integration demo
python demo_sqlite.py

# Show database schema
python demo_sqlite.py schema
```

---

## 🌐 Testing Scenarios

### **Scenario 1: New Customer Registration**
1. Go to `http://localhost:5000`
2. Click "Register"
3. Fill out registration form
4. Login with new credentials
5. Browse products and add to cart

### **Scenario 2: Product Shopping**
1. Login as `testuser` / `test123`
2. Visit "Products" page
3. Use search: try "headphones"
4. Filter by category: "Electronics"
5. Click on a product to view details
6. Add product to cart
7. View cart and proceed to checkout

### **Scenario 3: Admin Management**
1. Login as `admin` / `admin123`
2. Visit `/admin` for dashboard
3. View product and order statistics
4. Check recent orders and products

### **Scenario 4: Order Processing**
1. Login as customer
2. Add multiple products to cart
3. Go to checkout
4. Fill in shipping information
5. **Note**: Payment will fail without real Stripe keys
6. View order in order history

---

## 🐛 Troubleshooting

### **Common Issues**

#### **1. Import Errors**
```bash
# If you see circular import errors, restart the application
python app.py
```

#### **2. Database Issues**
```bash
# Reset database if corrupted
python database.py reset
python setup_database.py
```

#### **3. Missing Dependencies**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

#### **4. Port Already in Use**
```bash
# Kill process using port 5000
sudo lsof -t -i tcp:5000 | xargs kill -9

# Or run on different port
python -c "from app import app; app.run(port=5001)"
```

### **Debug Mode**
The application runs in debug mode by default, which provides:
- Automatic reloading on code changes
- Detailed error messages
- Interactive debugger in browser

---

## 📊 Testing Data

### **Sample Products (19 total)**
- Electronics: Headphones, Phone Cases, Cables, Charging Pads
- Clothing: T-Shirts, Jeans, Jackets, Sneakers
- Books: Programming, Web Development, Marketing guides
- Home & Garden: Desk Lamps, Plant Pots, Security Cameras
- Sports: Yoga Mats, Water Bottles, Resistance Bands
- Health & Beauty: Vitamin Serum, Electric Toothbrush

### **Sample Categories (6 total)**
- Electronics
- Clothing & Fashion
- Books & Media
- Home & Garden
- Sports & Outdoors
- Health & Beauty

---

## 🔍 API Testing

### **Manual API Testing**
You can test API endpoints directly:

```bash
# Get all products (requires login)
curl -X GET http://localhost:5000/products

# Add to cart (requires authentication)
curl -X POST http://localhost:5000/add_to_cart/1 \
  -d "quantity=2" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

### **Database Queries**
```bash
# Test database queries
python sqlite_browser.py
> SELECT * FROM product WHERE price < 30;
> SELECT u.username, COUNT(o.id) as order_count FROM user u LEFT JOIN "order" o ON u.id = o.user_id GROUP BY u.id;
```

---

## 🚀 Production Testing

### **Performance Testing**
```bash
# Install testing tools
pip install locust

# Create simple load test
# (You would need to create a locustfile.py)
```

### **Security Testing**
- Test SQL injection protection
- Verify password hashing
- Check session management
- Test CSRF protection

---

## 📝 Test Checklist

### **✅ Basic Functionality**
- [ ] Application starts without errors
- [ ] Database initializes correctly
- [ ] Home page loads
- [ ] User registration works
- [ ] User login/logout works
- [ ] Products display correctly
- [ ] Search functionality works
- [ ] Cart operations work
- [ ] Admin dashboard accessible

### **✅ Database Operations**
- [ ] Database utilities work
- [ ] Backup creation works
- [ ] SQLite browser functions
- [ ] Data integrity maintained
- [ ] Foreign key relationships work

### **✅ Error Handling**
- [ ] Graceful error messages
- [ ] Invalid login attempts handled
- [ ] Database errors caught
- [ ] 404 pages work
- [ ] Form validation works

---

## 🎯 Next Steps

After basic testing:

1. **Add Stripe Keys**: Get real Stripe API keys for payment testing
2. **Email Setup**: Configure email for order confirmations
3. **File Uploads**: Test product image uploads
4. **Advanced Features**: Add product reviews, wishlist, etc.
5. **Production Deploy**: Deploy to cloud platform

---

## 📞 Support

If you encounter issues:

1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure database is properly initialized
4. Check file permissions
5. Review the troubleshooting section above

**Happy Testing! 🎉**
