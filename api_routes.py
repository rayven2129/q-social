from flask import request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from flask_login import login_required, current_user
from models import Product, Category, CartItem, Order, OrderItem, User
from extensions import db
import stripe
import os

# Initialize API
api = Api(
    title='E-Commerce Platform API',
    version='1.0',
    description='A comprehensive e-commerce API with product catalog, cart management, and order processing',
    doc='/api/docs/',
    prefix='/api/v1'
)

# Namespaces
products_ns = Namespace('products', description='Product operations')
categories_ns = Namespace('categories', description='Category operations')
cart_ns = Namespace('cart', description='Shopping cart operations')
orders_ns = Namespace('orders', description='Order management')
auth_ns = Namespace('auth', description='Authentication operations')

api.add_namespace(products_ns)
api.add_namespace(categories_ns)
api.add_namespace(cart_ns)
api.add_namespace(orders_ns)
api.add_namespace(auth_ns)

# Models for Swagger documentation
category_model = api.model('Category', {
    'id': fields.Integer(required=True, description='Category ID'),
    'name': fields.String(required=True, description='Category name'),
    'description': fields.String(description='Category description')
})

product_model = api.model('Product', {
    'id': fields.Integer(required=True, description='Product ID'),
    'name': fields.String(required=True, description='Product name'),
    'description': fields.String(description='Product description'),
    'price': fields.Float(required=True, description='Product price'),
    'stock_quantity': fields.Integer(required=True, description='Available stock'),
    'category_id': fields.Integer(required=True, description='Category ID'),
    'category': fields.Nested(category_model, description='Product category'),
    'image_url': fields.String(description='Product image URL'),
    'is_active': fields.Boolean(description='Product availability status')
})

cart_item_model = api.model('CartItem', {
    'id': fields.Integer(required=True, description='Cart item ID'),
    'product_id': fields.Integer(required=True, description='Product ID'),
    'product': fields.Nested(product_model, description='Product details'),
    'quantity': fields.Integer(required=True, description='Item quantity'),
    'subtotal': fields.Float(description='Item subtotal')
})

order_item_model = api.model('OrderItem', {
    'id': fields.Integer(required=True, description='Order item ID'),
    'product_id': fields.Integer(required=True, description='Product ID'),
    'product_name': fields.String(required=True, description='Product name'),
    'quantity': fields.Integer(required=True, description='Item quantity'),
    'price': fields.Float(required=True, description='Item price'),
    'subtotal': fields.Float(description='Item subtotal')
})

order_model = api.model('Order', {
    'id': fields.Integer(required=True, description='Order ID'),
    'user_id': fields.Integer(required=True, description='User ID'),
    'total_amount': fields.Float(required=True, description='Order total'),
    'status': fields.String(required=True, description='Order status'),
    'created_at': fields.DateTime(description='Order creation date'),
    'items': fields.List(fields.Nested(order_item_model), description='Order items')
})

user_model = api.model('User', {
    'id': fields.Integer(required=True, description='User ID'),
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email address'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

# Input models
add_to_cart_input = api.model('AddToCart', {
    'product_id': fields.Integer(required=True, description='Product ID'),
    'quantity': fields.Integer(required=True, description='Quantity to add', min=1)
})

update_cart_input = api.model('UpdateCart', {
    'quantity': fields.Integer(required=True, description='New quantity', min=0)
})

# Products API
@products_ns.route('/')
class ProductList(Resource):
    @products_ns.doc('list_products')
    @products_ns.marshal_list_with(product_model)
    @products_ns.param('category', 'Filter by category ID')
    @products_ns.param('search', 'Search products by name or description')
    @products_ns.param('limit', 'Limit number of results')
    def get(self):
        """Fetch all products with optional filtering"""
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
        return products

@products_ns.route('/<int:product_id>')
@products_ns.param('product_id', 'Product identifier')
class ProductDetail(Resource):
    @products_ns.doc('get_product')
    @products_ns.marshal_with(product_model)
    def get(self, product_id):
        """Fetch a specific product by ID"""
        product = Product.query.get_or_404(product_id)
        if not product.is_active:
            api.abort(404, "Product not found or inactive")
        return product

# Categories API
@categories_ns.route('/')
class CategoryList(Resource):
    @categories_ns.doc('list_categories')
    @categories_ns.marshal_list_with(category_model)
    def get(self):
        """Fetch all categories"""
        categories = Category.query.all()
        return categories

@categories_ns.route('/<int:category_id>')
@categories_ns.param('category_id', 'Category identifier')
class CategoryDetail(Resource):
    @categories_ns.doc('get_category')
    @categories_ns.marshal_with(category_model)
    def get(self, category_id):
        """Fetch a specific category by ID"""
        category = Category.query.get_or_404(category_id)
        return category

@categories_ns.route('/<int:category_id>/products')
@categories_ns.param('category_id', 'Category identifier')
class CategoryProducts(Resource):
    @categories_ns.doc('get_category_products')
    @categories_ns.marshal_list_with(product_model)
    def get(self, category_id):
        """Fetch all products in a specific category"""
        category = Category.query.get_or_404(category_id)
        products = Product.query.filter_by(category_id=category_id, is_active=True).all()
        return products

# Cart API
@cart_ns.route('/')
class CartList(Resource):
    @cart_ns.doc('get_cart')
    @cart_ns.marshal_list_with(cart_item_model)
    @login_required
    def get(self):
        """Get current user's cart items"""
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        return cart_items

    @cart_ns.doc('add_to_cart')
    @cart_ns.expect(add_to_cart_input)
    @login_required
    def post(self):
        """Add item to cart"""
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        product = Product.query.get_or_404(product_id)
        if not product.is_active:
            api.abort(400, "Product is not available")
        
        if quantity > product.stock_quantity:
            api.abort(400, "Insufficient stock")
        
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
        return {'message': 'Item added to cart successfully'}, 201

@cart_ns.route('/<int:item_id>')
@cart_ns.param('item_id', 'Cart item identifier')
class CartItem(Resource):
    @cart_ns.doc('update_cart_item')
    @cart_ns.expect(update_cart_input)
    @login_required
    def put(self, item_id):
        """Update cart item quantity"""
        data = request.get_json()
        quantity = data.get('quantity')
        
        cart_item = CartItem.query.filter_by(
            id=item_id, 
            user_id=current_user.id
        ).first_or_404()
        
        if quantity == 0:
            db.session.delete(cart_item)
        else:
            if quantity > cart_item.product.stock_quantity:
                api.abort(400, "Insufficient stock")
            cart_item.quantity = quantity
        
        db.session.commit()
        return {'message': 'Cart updated successfully'}

    @cart_ns.doc('remove_cart_item')
    @login_required
    def delete(self, item_id):
        """Remove item from cart"""
        cart_item = CartItem.query.filter_by(
            id=item_id, 
            user_id=current_user.id
        ).first_or_404()
        
        db.session.delete(cart_item)
        db.session.commit()
        return {'message': 'Item removed from cart'}

# Orders API
@orders_ns.route('/')
class OrderList(Resource):
    @orders_ns.doc('list_orders')
    @orders_ns.marshal_list_with(order_model)
    @login_required
    def get(self):
        """Get current user's orders"""
        orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
        return orders

@orders_ns.route('/<int:order_id>')
@orders_ns.param('order_id', 'Order identifier')
class OrderDetail(Resource):
    @orders_ns.doc('get_order')
    @orders_ns.marshal_with(order_model)
    @login_required
    def get(self, order_id):
        """Get specific order details"""
        order = Order.query.filter_by(
            id=order_id, 
            user_id=current_user.id
        ).first_or_404()
        return order

# Auth API
@auth_ns.route('/profile')
class UserProfile(Resource):
    @auth_ns.doc('get_profile')
    @auth_ns.marshal_with(user_model)
    @login_required
    def get(self):
        """Get current user profile"""
        return current_user

# Payment API
payment_intent_input = api.model('PaymentIntent', {
    'amount': fields.Float(required=True, description='Payment amount in dollars')
})

@api.route('/payment/create-intent')
class CreatePaymentIntent(Resource):
    @api.doc('create_payment_intent')
    @api.expect(payment_intent_input)
    @login_required
    def post(self):
        """Create Stripe payment intent"""
        try:
            data = request.get_json()
            amount = int(data.get('amount', 0) * 100)  # Convert to cents
            
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                metadata={'user_id': current_user.id}
            )
            
            return {
                'client_secret': intent.client_secret,
                'amount': amount
            }
        except Exception as e:
            api.abort(400, str(e))

# Health check endpoint
@api.route('/health')
class HealthCheck(Resource):
    @api.doc('health_check')
    def get(self):
        """API health check"""
        return {
            'status': 'healthy',
            'message': 'E-Commerce API is running',
            'version': '1.0'
        }
