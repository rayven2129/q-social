from flask import Blueprint, request, jsonify, render_template_string
from flask_login import login_required, current_user
from models import Product, Category, CartItem, Order, OrderItem, User
from extensions import db
import stripe
import os

# Create API Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Simple Swagger-like documentation template
SWAGGER_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>E-Commerce API Documentation</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .method { display: inline-block; padding: 5px 10px; border-radius: 3px; color: white; font-weight: bold; }
        .get { background: #61affe; }
        .post { background: #49cc90; }
        .put { background: #fca130; }
        .delete { background: #f93e3e; }
        .auth-required { color: #ff6b6b; font-size: 12px; }
        pre { background: #f8f8f8; padding: 10px; border-radius: 3px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>🚀 E-Commerce API Documentation</h1>
    <p>Base URL: <code>/api/v1</code></p>
    
    <h2>📦 Products</h2>
    <div class="endpoint">
        <span class="method get">GET</span> <code>/products/</code>
        <p>Get all products with optional filtering</p>
        <p><strong>Query Parameters:</strong></p>
        <ul>
            <li><code>category</code> - Filter by category ID</li>
            <li><code>search</code> - Search by name or description</li>
            <li><code>limit</code> - Limit results (default: 50)</li>
        </ul>
    </div>
    
    <div class="endpoint">
        <span class="method get">GET</span> <code>/products/{id}</code>
        <p>Get specific product by ID</p>
    </div>
    
    <h2>🏷️ Categories</h2>
    <div class="endpoint">
        <span class="method get">GET</span> <code>/categories/</code>
        <p>Get all categories</p>
    </div>
    
    <div class="endpoint">
        <span class="method get">GET</span> <code>/categories/{id}</code>
        <p>Get specific category by ID</p>
    </div>
    
    <h2>🛒 Cart <span class="auth-required">(Authentication Required)</span></h2>
    <div class="endpoint">
        <span class="method get">GET</span> <code>/cart/</code>
        <p>Get current user's cart items</p>
    </div>
    
    <div class="endpoint">
        <span class="method post">POST</span> <code>/cart/</code>
        <p>Add item to cart</p>
        <pre>{"product_id": 1, "quantity": 2}</pre>
    </div>
    
    <div class="endpoint">
        <span class="method put">PUT</span> <code>/cart/{id}</code>
        <p>Update cart item quantity</p>
        <pre>{"quantity": 3}</pre>
    </div>
    
    <div class="endpoint">
        <span class="method delete">DELETE</span> <code>/cart/{id}</code>
        <p>Remove item from cart</p>
    </div>
    
    <h2>📋 Orders <span class="auth-required">(Authentication Required)</span></h2>
    <div class="endpoint">
        <span class="method get">GET</span> <code>/orders/</code>
        <p>Get user's order history</p>
    </div>
    
    <div class="endpoint">
        <span class="method get">GET</span> <code>/orders/{id}</code>
        <p>Get specific order details</p>
    </div>
    
    <h2>👤 Authentication <span class="auth-required">(Authentication Required)</span></h2>
    <div class="endpoint">
        <span class="method get">GET</span> <code>/auth/profile</code>
        <p>Get current user profile</p>
    </div>
    
    <h2>❤️ Health</h2>
    <div class="endpoint">
        <span class="method get">GET</span> <code>/health</code>
        <p>API health check</p>
    </div>
    
    <h2>💳 Payment <span class="auth-required">(Authentication Required)</span></h2>
    <div class="endpoint">
        <span class="method post">POST</span> <code>/payment/create-intent</code>
        <p>Create Stripe payment intent</p>
        <pre>{"amount": 29.99}</pre>
    </div>
    
    <h2>🧪 Testing</h2>
    <p>You can test these endpoints using:</p>
    <ul>
        <li><strong>cURL:</strong> <code>curl -X GET http://localhost:5000/api/v1/health</code></li>
        <li><strong>JavaScript:</strong> <code>fetch('/api/v1/products/').then(r => r.json())</code></li>
        <li><strong>Postman:</strong> Import the endpoints above</li>
        <li><strong>Web Interface:</strong> <a href="/api-docs">API Testing Page</a></li>
    </ul>
</body>
</html>
'''

# Documentation route
@api_bp.route('/docs/')
def api_docs():
    """Simple API documentation"""
    return render_template_string(SWAGGER_TEMPLATE)

# Products API
@api_bp.route('/products/', methods=['GET'])
def get_products():
    """Get all products with optional filtering"""
    try:
        category_id = request.args.get('category', type=int)
        search = request.args.get('search', '').strip()
        limit = request.args.get('limit', type=int, default=50)
        
        query = Product.query.filter_by(is_active=True)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if search:
            query = query.filter(Product.name.contains(search) | 
                               Product.description.contains(search))
        
        products = query.limit(limit).all()
        
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': float(p.price),
            'stock_quantity': p.stock_quantity,
            'category_id': p.category_id,
            'category': {'id': p.category.id, 'name': p.category.name} if p.category else None,
            'image_url': p.image_url,
            'is_active': p.is_active
        } for p in products])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    try:
        product = Product.query.get_or_404(product_id)
        if not product.is_active:
            return jsonify({'error': 'Product not found or inactive'}), 404
        
        return jsonify({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'stock_quantity': product.stock_quantity,
            'category_id': product.category_id,
            'category': {'id': product.category.id, 'name': product.category.name} if product.category else None,
            'image_url': product.image_url,
            'is_active': product.is_active
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Categories API
@api_bp.route('/categories/', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        categories = Category.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'description': c.description
        } for c in categories])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get a specific category by ID"""
    try:
        category = Category.query.get_or_404(category_id)
        return jsonify({
            'id': category.id,
            'name': category.name,
            'description': category.description
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Cart API
@api_bp.route('/cart/', methods=['GET'])
@login_required
def get_cart():
    """Get current user's cart items"""
    try:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        return jsonify([{
            'id': item.id,
            'product_id': item.product_id,
            'quantity': item.quantity,
            'subtotal': float(item.quantity * item.product.price),
            'product': {
                'id': item.product.id,
                'name': item.product.name,
                'price': float(item.product.price),
                'image_url': item.product.image_url
            }
        } for item in cart_items])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/cart/', methods=['POST'])
@login_required
def add_to_cart():
    """Add item to cart"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if not product_id or quantity < 1:
            return jsonify({'error': 'Invalid product_id or quantity'}), 400
        
        product = Product.query.get_or_404(product_id)
        if not product.is_active:
            return jsonify({'error': 'Product is not available'}), 400
        
        if quantity > product.stock_quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        # Check if item already in cart
        cart_item = CartItem.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                user_id=current_user.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        return jsonify({'message': 'Item added to cart successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/cart/<int:item_id>', methods=['PUT'])
@login_required
def update_cart_item(item_id):
    """Update cart item quantity"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        quantity = data.get('quantity')
        if quantity is None or quantity < 0:
            return jsonify({'error': 'Invalid quantity'}), 400
        
        cart_item = CartItem.query.filter_by(
            id=item_id, 
            user_id=current_user.id
        ).first_or_404()
        
        if quantity == 0:
            db.session.delete(cart_item)
        else:
            if quantity > cart_item.product.stock_quantity:
                return jsonify({'error': 'Insufficient stock'}), 400
            cart_item.quantity = quantity
        
        db.session.commit()
        return jsonify({'message': 'Cart updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/cart/<int:item_id>', methods=['DELETE'])
@login_required
def remove_cart_item(item_id):
    """Remove item from cart"""
    try:
        cart_item = CartItem.query.filter_by(
            id=item_id, 
            user_id=current_user.id
        ).first_or_404()
        
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item removed from cart'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Orders API
@api_bp.route('/orders/', methods=['GET'])
@login_required
def get_orders():
    """Get current user's orders"""
    try:
        orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
        return jsonify([{
            'id': order.id,
            'total_amount': float(order.total_amount),
            'status': order.status,
            'created_at': order.created_at.isoformat()
        } for order in orders])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/orders/<int:order_id>', methods=['GET'])
@login_required
def get_order(order_id):
    """Get specific order details"""
    try:
        order = Order.query.filter_by(
            id=order_id, 
            user_id=current_user.id
        ).first_or_404()
        
        return jsonify({
            'id': order.id,
            'total_amount': float(order.total_amount),
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'items': [{
                'id': item.id,
                'product_name': item.product_name,
                'quantity': item.quantity,
                'price': float(item.price)
            } for item in order.items]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# User profile
@api_bp.route('/auth/profile', methods=['GET'])
@login_required
def get_profile():
    """Get current user profile"""
    try:
        return jsonify({
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Payment API
@api_bp.route('/payment/create-intent', methods=['POST'])
@login_required
def create_payment_intent():
    """Create Stripe payment intent"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        amount = data.get('amount', 0)
        if amount <= 0:
            return jsonify({'error': 'Invalid amount'}), 400
        
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency='usd',
            metadata={'user_id': current_user.id}
        )
        
        return jsonify({
            'client_secret': intent.client_secret,
            'amount': int(amount * 100)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Health check
@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'message': 'E-Commerce API is running',
        'version': '1.0'
    })
