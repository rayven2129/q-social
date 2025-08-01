from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import app, stripe, STRIPE_PUBLISHABLE_KEY
from extensions import db
from models import User, Product, Category, CartItem, Order, OrderItem
import os
from decimal import Decimal

# Home page
@app.route('/')
def index():
    products = Product.query.filter_by(is_active=True).limit(8).all()
    categories = Category.query.all()
    return render_template('index.html', products=products, categories=categories)

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
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
        
        flash('Registration successful')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Product routes
@app.route('/products')
def products():
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    
    query = Product.query.filter_by(is_active=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(Product.name.contains(search))
    
    products = query.all()
    categories = Category.query.all()
    
    return render_template('products.html', products=products, categories=categories)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

# Cart routes
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Item added to cart')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        flash('Unauthorized')
        return redirect(url_for('cart'))
    
    quantity = int(request.form['quantity'])
    
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        flash('Unauthorized')
        return redirect(url_for('cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart')
    return redirect(url_for('cart'))

# Checkout and payment routes
@app.route('/checkout')
@login_required
def checkout():
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
            
            # Create order items
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

# Order routes
@app.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=user_orders)

@app.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        flash('Unauthorized')
        return redirect(url_for('orders'))
    
    return render_template('order_detail.html', order=order)

# Admin routes (basic)
@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    
    products = Product.query.all()
    orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    return render_template('admin.html', products=products, orders=orders)
