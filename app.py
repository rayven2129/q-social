from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import stripe
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ecommerce.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# SQLite specific configuration
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Stripe configuration
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_dummy_key')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', 'pk_test_dummy_key')

# Initialize extensions
from extensions import db, login_manager
from flask_cors import CORS

db.init_app(app)
login_manager.init_app(app)

# Enable CORS for API endpoints
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Import models and routes after app initialization
from models import User, Product, Category, CartItem, Order, OrderItem

# Register API Blueprint
from api_routes import api_bp
app.register_blueprint(api_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    """Home page with featured products and categories."""
    products = Product.query.filter_by(is_active=True).limit(8).all()
    categories = Category.query.all()
    return render_template('index.html', products=products, categories=categories)

@app.route('/products')
def products():
    """Products page with filtering and search."""
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '').strip()
    
    query = Product.query.filter_by(is_active=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(Product.name.contains(search) | Product.description.contains(search))
    
    products = query.all()
    categories = Category.query.all()
    
    return render_template('products.html', products=products, categories=categories)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Individual product detail page."""
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        
        # Validation
        if not all([username, email, password, first_name, last_name]):
            flash('All fields are required')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """Add product to cart."""
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if quantity <= 0:
        flash('Invalid quantity')
        return redirect(url_for('product_detail', product_id=product_id))
    
    if quantity > product.stock_quantity:
        flash(f'Only {product.stock_quantity} items available')
        return redirect(url_for('product_detail', product_id=product_id))
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock_quantity:
            flash(f'Cannot add more items. Only {product.stock_quantity} available.')
            return redirect(url_for('product_detail', product_id=product_id))
        cart_item.quantity = new_quantity
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'{product.name} added to cart!')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/cart')
@login_required
def cart():
    """View shopping cart."""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    """Update cart item quantity."""
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        flash('Unauthorized access')
        return redirect(url_for('cart'))
    
    quantity = int(request.form.get('quantity', 0))
    
    if quantity <= 0:
        db.session.delete(cart_item)
        flash('Item removed from cart')
    elif quantity > cart_item.product.stock_quantity:
        flash(f'Only {cart_item.product.stock_quantity} items available')
        return redirect(url_for('cart'))
    else:
        cart_item.quantity = quantity
        flash('Cart updated')
    
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    """Remove item from cart."""
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        flash('Unauthorized access')
        return redirect(url_for('cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart')
    return redirect(url_for('cart'))

@app.route('/checkout')
@login_required
def checkout():
    """Checkout page."""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty')
        return redirect(url_for('cart'))
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total, 
                         stripe_publishable_key=STRIPE_PUBLISHABLE_KEY)

@app.route('/create_payment_intent', methods=['POST'])
@login_required
def create_payment_intent():
    """Create Stripe payment intent."""
    try:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        total = sum(item.product.price * item.quantity for item in cart_items)
        
        # Create payment intent with Stripe
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),  # Amount in cents
            currency='usd',
            metadata={
                'user_id': current_user.id,
                'user_email': current_user.email
            }
        )
        
        return jsonify({
            'client_secret': intent.client_secret
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/confirm_payment', methods=['POST'])
@login_required
def confirm_payment():
    """Confirm payment and create order."""
    try:
        data = request.get_json()
        payment_intent_id = data['payment_intent_id']
        shipping_address = data['shipping_address']
        
        # Verify payment with Stripe
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if intent.status == 'succeeded':
            # Create order
            cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
            total = sum(item.product.price * item.quantity for item in cart_items)
            
            order = Order(
                user_id=current_user.id,
                total_amount=total,
                status='paid',
                payment_intent_id=payment_intent_id,
                shipping_address=shipping_address
            )
            
            db.session.add(order)
            db.session.flush()  # Get order ID
            
            # Create order items and update stock
            for cart_item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                db.session.add(order_item)
                
                # Update product stock
                cart_item.product.stock_quantity -= cart_item.quantity
            
            # Clear cart
            CartItem.query.filter_by(user_id=current_user.id).delete()
            
            db.session.commit()
            
            return jsonify({'success': True, 'order_id': order.id})
        else:
            return jsonify({'error': 'Payment not successful'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/orders')
@login_required
def orders():
    """View order history."""
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=user_orders)

@app.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    """View order details."""
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access')
        return redirect(url_for('orders'))
    
    return render_template('order_detail.html', order=order)

@app.route('/admin')
@login_required
def admin():
    """Admin dashboard."""
    if not current_user.is_admin:
        flash('Access denied - Admin privileges required')
        return redirect(url_for('index'))
    
    products = Product.query.all()
    orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    stats = {
        'total_users': User.query.count(),
        'total_products': Product.query.count(),
        'total_orders': Order.query.count(),
        'active_products': Product.query.filter_by(is_active=True).count(),
    }
    
    return render_template('admin.html', products=products, orders=orders, stats=stats)

@app.route('/api-docs')
def api_documentation():
    """API documentation page."""
    return render_template('api_docs.html')

@app.route('/api-test')
def api_test_interface():
    """Interactive API testing interface."""
    return render_template('api_test_interface.html')

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    print("🚀 Starting E-Commerce Platform...")
    print("📁 Database:", app.config['SQLALCHEMY_DATABASE_URI'])
    print("🌐 Server: http://localhost:5000")
    print("📚 API Documentation: http://localhost:5000/api/v1/docs/")
    print("🧪 Interactive API Testing: http://localhost:5000/api-test")
    print("🔧 API Base URL: http://localhost:5000/api/v1")
    print("👤 Test accounts:")
    print("   Admin: admin / admin123")
    print("   User:  testuser / test123")
    print("📂 Categories and products loaded!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
