# Installation Guide

## Python 3.13 Compatibility

This project has been updated to work with Python 3.13 using only stable, well-maintained packages.

### 1. Create Virtual Environment

```bash
# Navigate to project directory
cd q-social

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 2. Test Installation (Optional but Recommended)

```bash
# Test that all dependencies can be installed
python test_install.py
```

### 3. Install Dependencies

```bash
# Make sure you're in the virtual environment (you should see (venv) in your prompt)
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
# The .env file is already created, just edit it with your settings
# Edit .env file with your configuration:
# - Set a secure SECRET_KEY
# - Add your Stripe API keys (get from https://stripe.com)
```

### 5. Initialize Database

```bash
# Set up the database with sample data
python setup_database.py
```

### 6. Run the Application

```bash
python app.py
```

The application will be available at:
- **Main App**: http://localhost:5000
- **API Documentation**: http://localhost:5000/api/v1/docs/
- **API Testing Interface**: http://localhost:5000/api-docs

## API Features

### Simple Documentation
- Clean API documentation at `/api/v1/docs/`
- User-friendly testing interface at `/api-docs`
- No external dependencies - uses pure Flask

### Available Endpoints
- **Products**: `/api/v1/products/`
- **Categories**: `/api/v1/categories/`
- **Cart**: `/api/v1/cart/` (requires login)
- **Orders**: `/api/v1/orders/` (requires login)
- **Health Check**: `/api/v1/health`
- **User Profile**: `/api/v1/auth/profile` (requires login)
- **Payment**: `/api/v1/payment/create-intent` (requires login)

### Test Accounts
- **Admin**: username=`admin`, password=`admin123`
- **User**: username=`testuser`, password=`test123`

## Package Versions (Python 3.13 Compatible)

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.1
WTForms==3.1.1
Werkzeug==3.0.1
stripe==7.8.0
python-dotenv==1.0.0
email-validator==2.1.0
bcrypt==4.1.2
Pillow==10.1.0
tabulate==0.9.0
flask-cors==4.0.0
```

## Troubleshooting

### Virtual Environment Issues
If you get "externally-managed-environment" error:
1. Make sure you're in a virtual environment: `source venv/bin/activate`
2. Check that `(venv)` appears in your terminal prompt
3. If still having issues, recreate the virtual environment

### Package Installation Issues
If you encounter package installation errors:
1. Update pip: `pip install --upgrade pip`
2. Run the test script: `python test_install.py`
3. Try installing packages individually if needed
4. Check Python version: `python --version` (should be 3.13.x)

### Database Issues
If database errors occur:
1. Delete `ecommerce.db` file
2. Run `python setup_database.py` again
3. Check that SQLite is properly installed

## Development

### API Testing
1. Start the server: `python app.py`
2. Visit http://localhost:5000/api/v1/docs/ for documentation
3. Use the test interface at http://localhost:5000/api-docs
4. Test with curl or any HTTP client

### Example API Calls
```bash
# Health check
curl -X GET http://localhost:5000/api/v1/health

# Get all products
curl -X GET http://localhost:5000/api/v1/products/

# Get categories
curl -X GET http://localhost:5000/api/v1/categories/
```

### Adding New API Endpoints
1. Add routes to `api_routes.py`
2. Follow the existing pattern for consistent API design
3. Add error handling with try/catch blocks
4. Return JSON responses with appropriate HTTP status codes

## Production Deployment

For production deployment:
1. Set `FLASK_ENV=production` in environment
2. Use a production WSGI server like Gunicorn
3. Configure a proper database (PostgreSQL/MySQL)
4. Set up HTTPS and proper security headers
5. Use environment variables for all sensitive configuration

## What's Different from Complex Swagger Setups

This implementation uses a **simpler, more reliable approach**:
- ✅ **No external Swagger dependencies** that might break with Python 3.13
- ✅ **Pure Flask** with built-in JSON responses
- ✅ **Custom documentation page** that's always compatible
- ✅ **All API functionality preserved**
- ✅ **Easier to maintain and debug**
- ✅ **Faster installation** with fewer dependencies
