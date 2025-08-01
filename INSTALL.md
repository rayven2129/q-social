# Installation Guide - Python 3.13 Compatible

## Quick Start (Recommended)

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

### 2. Use the Smart Installer (Handles Python 3.13 Issues)

```bash
# Run the smart installer that handles compatibility issues
python install.py
```

This installer will:
- ✅ Check your virtual environment
- ✅ Upgrade pip automatically
- ✅ Install packages one by one with error handling
- ✅ Skip problematic packages (like Pillow) gracefully
- ✅ Give you a detailed report of what worked

### 3. Test Installation

```bash
# Verify everything is working
python test_install.py
```

### 4. Set Up and Run

```bash
# Initialize database
python setup_database.py

# Start the application
python app.py
```

## Alternative Installation Methods

### Method 2: Minimal Requirements (If Smart Installer Fails)

```bash
# Install only essential packages
pip install --upgrade pip
pip install -r requirements-minimal.txt
```

### Method 3: Manual Installation (For Troubleshooting)

```bash
# Install packages individually
pip install Flask>=3.0.0
pip install Flask-SQLAlchemy>=3.1.0
pip install Flask-Login>=0.6.0
pip install Flask-WTF>=1.2.0
pip install WTForms>=3.1.0
pip install Werkzeug>=3.0.0
pip install stripe>=8.0.0
pip install python-dotenv>=1.0.0
pip install email-validator>=2.1.0
pip install bcrypt>=4.1.0
pip install tabulate>=0.9.0
pip install flask-cors>=4.0.0

# Optional (may fail on Python 3.13)
pip install Pillow>=10.0.0  # Skip if this fails
```

## Application URLs

Once running, access:
- **Main App**: http://localhost:5000
- **API Documentation**: http://localhost:5000/api/v1/docs/
- **API Testing Interface**: http://localhost:5000/api-docs

## Test Accounts
- **Admin**: username=`admin`, password=`admin123`
- **User**: username=`testuser`, password=`test123`

## What's Different About This Setup

### Python 3.13 Compatibility Issues Solved
- ✅ **Smart installer** handles package conflicts
- ✅ **Pillow made optional** (not needed for API functionality)
- ✅ **Latest stable versions** of all packages
- ✅ **Graceful error handling** for problematic packages

### Package Versions (Tested with Python 3.13)
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.1
WTForms==3.1.1
Werkzeug==3.0.1
stripe==8.0.0
python-dotenv==1.0.0
email-validator==2.1.0
bcrypt==4.1.2
tabulate==0.9.0
flask-cors==4.0.0
Pillow==10.2.0  # Optional
```

## Troubleshooting

### If Smart Installer Reports Failures
1. **Check the error messages** - the installer shows exactly what failed
2. **Try minimal requirements**: `pip install -r requirements-minimal.txt`
3. **Install manually** one package at a time
4. **Skip Pillow** if it fails (not needed for core functionality)

### Virtual Environment Issues
```bash
# Make sure you see (venv) in your prompt
# If not, reactivate:
source venv/bin/activate

# Verify you're in the right environment:
which python  # Should show path with /venv/
```

### Database Issues
```bash
# If database errors occur:
rm ecommerce.db  # Delete old database
python setup_database.py  # Recreate
```

### Package Conflicts
```bash
# If you get dependency conflicts:
pip install --upgrade pip
pip install --force-reinstall Flask>=3.0.0
```

## API Features

### Simple, Reliable Documentation
- **Custom docs page**: `/api/v1/docs/` (no external dependencies)
- **Interactive testing**: `/api-docs`
- **All endpoints working**: Products, Cart, Orders, Authentication

### Available Endpoints
- `GET /api/v1/products/` - List products
- `GET /api/v1/categories/` - List categories  
- `GET /api/v1/cart/` - Get cart (auth required)
- `POST /api/v1/cart/` - Add to cart (auth required)
- `GET /api/v1/orders/` - List orders (auth required)
- `GET /api/v1/health` - Health check

## Development

### Testing the API
```bash
# Health check
curl http://localhost:5000/api/v1/health

# Get products
curl http://localhost:5000/api/v1/products/

# Get categories
curl http://localhost:5000/api/v1/categories/
```

### Adding Features
1. Edit `api_routes.py` for new API endpoints
2. Edit `app.py` for new web routes
3. Edit `models.py` for database changes
4. Run `python setup_database.py` after model changes

## Why This Approach Works

### Advantages Over Complex Setups
- ✅ **No build errors** with Python 3.13
- ✅ **Faster installation** (handles failures gracefully)
- ✅ **More reliable** (fewer external dependencies)
- ✅ **Easier debugging** (clear error messages)
- ✅ **Production ready** (all core functionality works)

### What We Avoided
- ❌ Complex Swagger libraries with build issues
- ❌ Packages that don't support Python 3.13 yet
- ❌ Fragile dependency chains
- ❌ Hard-to-debug installation failures

This setup prioritizes **reliability and compatibility** over fancy features, ensuring you can actually run the application!
