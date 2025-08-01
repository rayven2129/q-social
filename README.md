# E-Commerce Platform

A full-featured e-commerce platform built with Python 3 and Flask, featuring user accounts, product catalog, shopping cart, and payment processing with Stripe.

## Features

- **User Authentication**: Registration, login, and user profiles
- **Product Catalog**: Browse products by category with search functionality
- **Shopping Cart**: Add, update, and remove items from cart
- **Payment Processing**: Secure payments using Stripe
- **Order Management**: Track orders and view order history
- **Admin Dashboard**: Basic admin interface for managing products and orders
- **Responsive Design**: Mobile-friendly interface using Bootstrap

## Technology Stack

- **Backend**: Python 3, Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (easily configurable for PostgreSQL/MySQL)
- **Payment**: Stripe API
- **Authentication**: Flask-Login

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd q-social
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file and add your configuration:
   - Set a secure `SECRET_KEY`
   - Add your Stripe API keys (get them from https://stripe.com)

5. **Initialize the database**:
   ```bash
   python setup_database.py
   ```

6. **Run the application**:
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

## SQLite Database

This project uses SQLite as the default database, which is perfect for development and small to medium-scale deployments.

### Database Features

- **File-based**: Database stored as `ecommerce.db` file
- **Zero configuration**: No database server setup required
- **ACID compliant**: Reliable transactions and data integrity
- **Cross-platform**: Works on Windows, macOS, and Linux

### Database Management

The project includes several utilities for managing the SQLite database:

#### Database Setup
```bash
# Complete database setup with sample data
python setup_database.py

# Alternative: Use the original sample data script
python sample_data.py
```

#### Database Utilities
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
```

#### SQLite Browser
Interactive database browser for exploring your data:
```bash
# Start interactive mode
python sqlite_browser.py

# Quick commands
python sqlite_browser.py tables          # List all tables
python sqlite_browser.py info            # Database information
python sqlite_browser.py schema users    # Show table schema
python sqlite_browser.py browse products 20  # Browse products (limit 20)
```

### Database Location

- **Development**: `ecommerce.db` in the project root
- **Production**: Configure via `DATABASE_URL` environment variable
- **Backups**: Stored in `backups/` directory with timestamps

## Configuration

### Environment Variables

- `SECRET_KEY`: Flask secret key for session management
- `DATABASE_URL`: Database connection string (default: SQLite)
- `STRIPE_PUBLISHABLE_KEY`: Stripe publishable key
- `STRIPE_SECRET_KEY`: Stripe secret key

### Stripe Setup

1. Create a Stripe account at https://stripe.com
2. Get your API keys from the Stripe dashboard
3. Add them to your `.env` file
4. For testing, use Stripe's test card numbers:
   - Success: `4242 4242 4242 4242`
   - Decline: `4000 0000 0000 0002`

## Usage

### Test Accounts

After running `sample_data.py`, you'll have these test accounts:

- **Admin**: username=`admin`, password=`admin123`
- **User**: username=`testuser`, password=`test123`

### Key Features

1. **Browse Products**: Visit the products page to see all available items
2. **Search & Filter**: Use the search bar and category filters
3. **Add to Cart**: Click on products to view details and add to cart
4. **Checkout**: Proceed through the secure checkout process
5. **Order Tracking**: View your order history and details
6. **Admin Panel**: Access admin features with the admin account

## Project Structure

```
q-social/
├── app.py              # Main Flask application
├── models.py           # Database models
├── routes.py           # Application routes
├── requirements.txt    # Python dependencies
├── sample_data.py      # Sample data generator
├── .env.example        # Environment variables template
├── templates/          # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── cart.html
│   ├── checkout.html
│   └── ...
├── static/             # Static files
│   ├── css/
│   ├── js/
│   └── uploads/
└── README.md
```

## Database Models

- **User**: Customer accounts and authentication
- **Category**: Product categories
- **Product**: Product information and inventory
- **CartItem**: Shopping cart items
- **Order**: Customer orders
- **OrderItem**: Individual items within orders

## API Endpoints

### Authentication
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout

### Products
- `GET /` - Home page with featured products
- `GET /products` - Product listing with search/filter
- `GET /product/<id>` - Product details

### Shopping Cart
- `POST /add_to_cart/<id>` - Add item to cart
- `GET /cart` - View cart
- `POST /update_cart/<id>` - Update cart item
- `GET /remove_from_cart/<id>` - Remove from cart

### Checkout & Orders
- `GET /checkout` - Checkout page
- `POST /create_payment_intent` - Create Stripe payment
- `POST /confirm_payment` - Confirm payment and create order
- `GET /orders` - Order history
- `GET /order/<id>` - Order details

### Admin
- `GET /admin` - Admin dashboard

## Security Features

- Password hashing using Werkzeug
- CSRF protection with Flask-WTF
- Secure session management
- Input validation and sanitization
- SQL injection prevention with SQLAlchemy ORM

## Customization

### Adding New Features

1. **Email Notifications**: Add Flask-Mail for order confirmations
2. **Product Reviews**: Extend models to include user reviews
3. **Inventory Management**: Add low stock alerts
4. **Shipping Integration**: Connect with shipping APIs
5. **Advanced Admin**: Full CRUD operations for products

### Styling

- Modify `static/css/style.css` for custom styling
- Update Bootstrap theme or add custom themes
- Customize templates in the `templates/` directory

## Deployment

### Production Considerations

1. **Database**: Use PostgreSQL or MySQL instead of SQLite
2. **Environment**: Set `FLASK_ENV=production`
3. **Security**: Use strong secret keys and HTTPS
4. **Static Files**: Serve static files with nginx or CDN
5. **Process Management**: Use Gunicorn with supervisor

### Example Production Setup

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues, please create an issue in the repository or contact the development team.
