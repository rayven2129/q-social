#!/usr/bin/env python3
"""
Test script to verify that all dependencies are installed correctly
"""

def test_imports():
    """Test that all required packages can be imported"""
    try:
        print("Testing core imports...")
        
        import flask
        print(f"✅ Flask {flask.__version__}")
        
        import flask_sqlalchemy
        print(f"✅ Flask-SQLAlchemy {flask_sqlalchemy.__version__}")
        
        import flask_login
        print(f"✅ Flask-Login {flask_login.__version__}")
        
        import flask_wtf
        print(f"✅ Flask-WTF {flask_wtf.__version__}")
        
        import wtforms
        print(f"✅ WTForms {wtforms.__version__}")
        
        import werkzeug
        print(f"✅ Werkzeug {werkzeug.__version__}")
        
        import stripe
        print(f"✅ Stripe {stripe.__version__}")
        
        import dotenv
        print("✅ python-dotenv")
        
        import email_validator
        print("✅ email-validator")
        
        import bcrypt
        print("✅ bcrypt")
        
        import tabulate
        print("✅ tabulate")
        
        import flask_cors
        print("✅ flask-cors")
        
        # Optional packages
        print("\nTesting optional imports...")
        try:
            import PIL
            print(f"✅ Pillow {PIL.__version__}")
        except ImportError:
            print("⚠️  Pillow not installed (optional - image processing)")
        
        print("\n🎉 All critical imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Critical import error: {e}")
        return False

def test_flask_app():
    """Test basic Flask app creation"""
    try:
        print("\nTesting Flask app creation...")
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/test')
        def test():
            return {'status': 'ok'}
        
        with app.test_client() as client:
            response = client.get('/test')
            assert response.status_code == 200
            
        print("✅ Flask app creation successful!")
        return True
        
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def test_database():
    """Test SQLAlchemy database functionality"""
    try:
        print("\nTesting database functionality...")
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db = SQLAlchemy(app)
        
        class TestModel(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(50))
        
        with app.app_context():
            db.create_all()
            
        print("✅ Database functionality working!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_authentication():
    """Test authentication packages"""
    try:
        print("\nTesting authentication packages...")
        
        import flask_login
        import bcrypt
        
        # Test bcrypt
        password = "test123"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        assert bcrypt.checkpw(password.encode('utf-8'), hashed)
        
        print("✅ Authentication packages working!")
        return True
        
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing E-Commerce Platform Dependencies\n")
    
    success = True
    success &= test_imports()
    success &= test_flask_app()
    success &= test_database()
    success &= test_authentication()
    
    if success:
        print("\n🎉 All tests passed! You're ready to run the application.")
        print("\nNext steps:")
        print("1. Set up your .env file with Stripe keys")
        print("2. Run: python setup_database.py")
        print("3. Run: python app.py")
        print("4. Visit: http://localhost:5000")
        print("5. API docs: http://localhost:5000/api/v1/docs/")
    else:
        print("\n❌ Some tests failed. Please check your installation.")
        print("\nTry running: python install.py")
        
    return success

if __name__ == '__main__':
    main()
