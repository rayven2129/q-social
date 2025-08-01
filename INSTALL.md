# Installation Guide

## Python 3.13 Compatibility

This project has been updated to work with Python 3.13. Follow these steps to set up the environment:

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

### 2. Install Dependencies

```bash
# Make sure you're in the virtual environment (you should see (venv) in your prompt)
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your configuration
# - Set a secure SECRET_KEY
# - Add your Stripe API keys (get from https://stripe.com)
```

### 4. Initialize Database

```bash
# Set up the database with sample data
python setup_database.py
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at:
- **Main App**: http://localhost:5000
- **API Documentation**: http://localhost:5000/api/docs/
- **API Testing Interface**: http://localhost:5000/api-docs

## API Features

### Swagger Documentation
- Interactive API documentation at `/api/docs/`
- User-friendly testing interface at `/api-docs`
- Full REST API with authentication support

### Available Endpoints
- **Products**: `/api/v1/products/`
- **Categories**: `/api/v1/categories/`
- **Cart**: `/api/v1/cart/` (requires login)
- **Orders**: `/api/v1/orders/` (requires login)
- **Health Check**: `/api/v1/health`

### Test Accounts
- **Admin**: username=`admin`, password=`admin123`
- **User**: username=`testuser`, password=`test123`

## Troubleshooting

### Virtual Environment Issues
If you get "externally-managed-environment" error:
1. Make sure you're in a virtual environment: `source venv/bin/activate`
2. Check that `(venv)` appears in your terminal prompt
3. If still having issues, recreate the virtual environment

### Package Installation Issues
If you encounter package installation errors:
1. Update pip: `pip install --upgrade pip`
2. Try installing packages individually if needed
3. Check Python version: `python --version` (should be 3.13.x)

### Database Issues
If database errors occur:
1. Delete `ecommerce.db` file
2. Run `python setup_database.py` again
3. Check that SQLite is properly installed

## Development

### API Testing
1. Start the server: `python app.py`
2. Visit http://localhost:5000/api/docs/ for Swagger UI
3. Use the test interface at http://localhost:5000/api-docs
4. Test with curl or any HTTP client

### Adding New API Endpoints
1. Add routes to `api_routes.py`
2. Use `@swag_from()` decorator for Swagger documentation
3. Follow the existing pattern for consistent API design

## Production Deployment

For production deployment:
1. Set `FLASK_ENV=production` in environment
2. Use a production WSGI server like Gunicorn
3. Configure a proper database (PostgreSQL/MySQL)
4. Set up HTTPS and proper security headers
5. Use environment variables for all sensitive configuration
