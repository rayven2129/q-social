from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from flasgger import swag_from
from models import Product, Category, CartItem, Order, OrderItem, User
from extensions import db
import stripe
import os

# Create API Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Products API
@api_bp.route('/products/', methods=['GET'])
@swag_from({
    'tags': ['Products'],
    'summary': 'Get all products',
    'description': 'Retrieve a list of all active products with optional filtering',
    'parameters': [
        {
            'name': 'category',
            'in': 'query',
            'type': 'integer',
            'description': 'Filter by category ID'
        },
        {
            'name': 'search',
            'in': 'query',
            'type': 'string',
            'description': 'Search products by name or description'
        },
        {
            'name': 'limit',
            'in': 'query',
            'type': 'integer',
            'description': 'Limit number of results (default: 50)'
        }
    ],
    'responses': {
        200: {
            'description': 'List of products',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'description': {'type': 'string'},
                        'price': {'type': 'number'},
                        'stock_quantity': {'type': 'integer'},
                        'category_id': {'type': 'integer'},
                        'image_url': {'type': 'string'},
                        'is_active': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def get_products():
    """Get all products with optional filtering"""
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

@api_bp.route('/products/<int:product_id>', methods=['GET'])
@swag_from({
    'tags': ['Products'],
    'summary': 'Get product by ID',
    'description': 'Retrieve a specific product by its ID',
    'parameters': [
        {
            'name': 'product_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Product ID'
        }
    ],
    'responses': {
        200: {
            'description': 'Product details',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'price': {'type': 'number'},
                    'stock_quantity': {'type': 'integer'},
                    'category_id': {'type': 'integer'},
                    'image_url': {'type': 'string'},
                    'is_active': {'type': 'boolean'}
                }
            }
        },
        404: {'description': 'Product not found'}
    }
})
def get_product(product_id):
    """Get a specific product by ID"""
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

# Categories API
@api_bp.route('/categories/', methods=['GET'])
@swag_from({
    'tags': ['Categories'],
    'summary': 'Get all categories',
    'description': 'Retrieve a list of all product categories',
    'responses': {
        200: {
            'description': 'List of categories',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'description': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_categories():
    """Get all categories"""
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description
    } for c in categories])

@api_bp.route('/categories/<int:category_id>', methods=['GET'])
@swag_from({
    'tags': ['Categories'],
    'summary': 'Get category by ID',
    'description': 'Retrieve a specific category by its ID',
    'parameters': [
        {
            'name': 'category_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Category ID'
        }
    ],
    'responses': {
        200: {
            'description': 'Category details',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'description': {'type': 'string'}
                }
            }
        },
        404: {'description': 'Category not found'}
    }
})
def get_category(category_id):
    """Get a specific category by ID"""
    category = Category.query.get_or_404(category_id)
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description
    })

# Cart API
@api_bp.route('/cart/', methods=['GET'])
@login_required
@swag_from({
    'tags': ['Cart'],
    'summary': 'Get cart items',
    'description': 'Get current user\'s cart items',
    'responses': {
        200: {
            'description': 'List of cart items',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'product_id': {'type': 'integer'},
                        'quantity': {'type': 'integer'},
                        'subtotal': {'type': 'number'},
                        'product': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'name': {'type': 'string'},
                                'price': {'type': 'number'}
                            }
                        }
                    }
                }
            }
        },
        401: {'description': 'Authentication required'}
    }
})
def get_cart():
    """Get current user's cart items"""
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

@api_bp.route('/cart/', methods=['POST'])
@login_required
@swag_from({
    'tags': ['Cart'],
    'summary': 'Add item to cart',
    'description': 'Add a product to the user\'s cart',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'product_id': {'type': 'integer', 'description': 'Product ID'},
                    'quantity': {'type': 'integer', 'description': 'Quantity to add', 'minimum': 1}
                },
                'required': ['product_id', 'quantity']
            }
        }
    ],
    'responses': {
        201: {'description': 'Item added to cart successfully'},
        400: {'description': 'Bad request - invalid data or insufficient stock'},
        401: {'description': 'Authentication required'},
        404: {'description': 'Product not found'}
    }
})
def add_to_cart():
    """Add item to cart"""
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

# Health check
@api_bp.route('/health', methods=['GET'])
@swag_from({
    'tags': ['Health'],
    'summary': 'API Health Check',
    'description': 'Check if the API is running properly',
    'responses': {
        200: {
            'description': 'API is healthy',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'message': {'type': 'string'},
                    'version': {'type': 'string'}
                }
            }
        }
    }
})
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'message': 'E-Commerce API is running',
        'version': '1.0'
    })

# Orders API
@api_bp.route('/orders/', methods=['GET'])
@login_required
@swag_from({
    'tags': ['Orders'],
    'summary': 'Get user orders',
    'description': 'Get current user\'s order history',
    'responses': {
        200: {
            'description': 'List of orders',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'total_amount': {'type': 'number'},
                        'status': {'type': 'string'},
                        'created_at': {'type': 'string', 'format': 'date-time'}
                    }
                }
            }
        },
        401: {'description': 'Authentication required'}
    }
})
def get_orders():
    """Get current user's orders"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return jsonify([{
        'id': order.id,
        'total_amount': float(order.total_amount),
        'status': order.status,
        'created_at': order.created_at.isoformat()
    } for order in orders])

# User profile
@api_bp.route('/auth/profile', methods=['GET'])
@login_required
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Get user profile',
    'description': 'Get current user\'s profile information',
    'responses': {
        200: {
            'description': 'User profile',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'}
                }
            }
        },
        401: {'description': 'Authentication required'}
    }
})
def get_profile():
    """Get current user profile"""
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name
    })
