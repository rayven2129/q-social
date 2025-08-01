# 🚀 How to Test and Run the E-Commerce Platform

## ⚡ Quick Start (5 Minutes)

### 1. **Setup Environment**
```bash
cd q-social
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. **Initialize Database**
```bash
python setup_database.py
```

### 3. **Run Application**
```bash
python app.py
```

### 4. **Open Browser**
Visit: **http://localhost:5000**

---

## 🧪 Automated Testing

Run the complete test suite:
```bash
source venv/bin/activate
python test_app.py
```

This tests:
- ✅ Module imports
- ✅ Database connectivity
- ✅ Sample data loading
- ✅ Flask application startup
- ✅ All web pages accessibility

---

## 👤 Test Accounts

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Administrator |
| `testuser` | `test123` | Customer |

---

## 🛍️ Features to Test

### **1. Customer Experience**
1. **Registration**: Create new account
2. **Login**: Sign in with test account
3. **Browse Products**: View 19 sample products across 6 categories
4. **Search**: Try searching for "headphones" or "shirt"
5. **Product Details**: Click on any product
6. **Add to Cart**: Add items to shopping cart
7. **Cart Management**: Update quantities, remove items
8. **Checkout**: Fill shipping info (payment will show demo)
9. **Order History**: View past orders

### **2. Admin Features**
1. **Login as Admin**: Use admin/admin123
2. **Admin Dashboard**: Visit `/admin`
3. **View Statistics**: See user, product, order counts
4. **Manage Data**: Overview of products and orders

### **3. Database Features**
```bash
# View database statistics
python database.py stats

# Browse database interactively
python sqlite_browser.py

# Create backup
python database.py backup

# View sample data
python demo_sqlite.py
```

---

## 🌐 Application URLs

- **Home**: http://localhost:5000/
- **Products**: http://localhost:5000/products
- **Login**: http://localhost:5000/login
- **Register**: http://localhost:5000/register
- **Cart**: http://localhost:5000/cart (requires login)
- **Orders**: http://localhost:5000/orders (requires login)
- **Admin**: http://localhost:5000/admin (requires admin login)

---

## 📊 Sample Data

### **Products (19 items)**
- **Electronics**: Headphones ($129.99), Phone Cases ($24.99), Cables ($15.99)
- **Clothing**: T-Shirts ($22.99), Jeans ($59.99), Jackets ($119.99)
- **Books**: Programming guides ($34.99-$44.99)
- **Home & Garden**: Desk lamps ($49.99), Plant pots ($34.99)
- **Sports**: Yoga mats ($29.99), Water bottles ($24.99)
- **Health & Beauty**: Vitamin serum ($27.99), Electric toothbrush ($69.99)

### **Categories (6 types)**
- Electronics, Clothing & Fashion, Books & Media
- Home & Garden, Sports & Outdoors, Health & Beauty

---

## 🔧 Troubleshooting

### **Common Issues**

#### **Port 5000 in use**
```bash
# Kill existing process
sudo lsof -t -i tcp:5000 | xargs kill -9

# Or use different port
python -c "from app import app; app.run(port=5001)"
```

#### **Database issues**
```bash
# Reset database
python database.py reset
python setup_database.py
```

#### **Import errors**
```bash
# Ensure virtual environment is active
source venv/bin/activate
pip install -r requirements.txt
```

#### **Permission errors**
```bash
# Fix file permissions
chmod +x *.py
```

---

## 🎯 Testing Scenarios

### **Scenario 1: New Customer Journey**
1. Visit home page
2. Click "Register" → Create account
3. Browse products → Add items to cart
4. Proceed to checkout → Fill shipping info
5. View order in order history

### **Scenario 2: Admin Management**
1. Login as admin (admin/admin123)
2. Visit `/admin` dashboard
3. Review statistics and recent orders
4. Check product inventory levels

### **Scenario 3: Database Operations**
1. Run `python database.py stats`
2. Create backup: `python database.py backup`
3. Browse data: `python sqlite_browser.py tables`
4. View schema: `python demo_sqlite.py schema`

---

## 📱 Mobile Testing

The application is responsive and works on mobile devices:
- Test on different screen sizes
- Check navigation menu collapse
- Verify touch interactions
- Test form inputs on mobile

---

## 🔍 Advanced Testing

### **Database Queries**
```bash
python sqlite_browser.py
> SELECT * FROM product WHERE price < 30;
> SELECT COUNT(*) FROM "order";
> SELECT u.username, COUNT(o.id) FROM user u LEFT JOIN "order" o ON u.id = o.user_id GROUP BY u.id;
```

### **API Testing**
```bash
# Test product API (requires authentication)
curl -X GET http://localhost:5000/products

# Test with authentication
curl -X POST http://localhost:5000/add_to_cart/1 \
  -d "quantity=2" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

---

## 🚀 Production Considerations

### **Before Production**
1. **Get Stripe Keys**: Replace dummy Stripe keys with real ones
2. **Set SECRET_KEY**: Use a secure random key
3. **Database**: Consider PostgreSQL for production
4. **HTTPS**: Enable SSL/TLS
5. **Email**: Configure SMTP for order confirmations

### **Environment Variables**
```bash
# Production .env example
SECRET_KEY=your-super-secure-secret-key
DATABASE_URL=postgresql://user:pass@localhost/ecommerce
STRIPE_PUBLISHABLE_KEY=pk_live_your_real_key
STRIPE_SECRET_KEY=sk_live_your_real_key
```

---

## 📈 Performance Testing

### **Load Testing**
```bash
# Install testing tools
pip install locust

# Create basic load test
# (Would require creating locustfile.py)
```

### **Database Performance**
```bash
# Optimize database
python database.py vacuum

# Check database size
python database.py stats
```

---

## ✅ Test Checklist

### **Basic Functionality**
- [ ] Application starts without errors
- [ ] Home page loads correctly
- [ ] User registration works
- [ ] User login/logout functions
- [ ] Products display properly
- [ ] Search functionality works
- [ ] Cart operations function
- [ ] Admin dashboard accessible
- [ ] Database operations work

### **User Experience**
- [ ] Navigation is intuitive
- [ ] Forms validate properly
- [ ] Error messages are clear
- [ ] Mobile interface works
- [ ] Page loading is reasonable

### **Data Integrity**
- [ ] User data saves correctly
- [ ] Product inventory updates
- [ ] Orders create properly
- [ ] Cart persists between sessions
- [ ] Database relationships work

---

## 🎉 Success Indicators

If everything works correctly, you should see:

1. **Application starts** with welcome message
2. **Database statistics** show sample data loaded
3. **All web pages** load without errors
4. **Test accounts** can login successfully
5. **Products display** with images and details
6. **Cart functionality** works smoothly
7. **Admin dashboard** shows statistics
8. **Database tools** function properly

---

## 📞 Getting Help

If you encounter issues:

1. **Check Console Output**: Look for error messages
2. **Run Tests**: Use `python test_app.py`
3. **Verify Setup**: Ensure all steps were followed
4. **Check Dependencies**: Run `pip install -r requirements.txt`
5. **Database Issues**: Try `python database.py reset`

**Happy Testing! 🎊**

The platform is production-ready with SQLite and can easily scale to PostgreSQL or MySQL when needed.
