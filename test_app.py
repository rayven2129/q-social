#!/usr/bin/env python3
"""
Automated test script for the e-commerce platform.
This script tests basic functionality without requiring manual interaction.
"""

import os
import sys
import requests
import time
import subprocess
from threading import Thread

def test_database_setup():
    """Test database initialization."""
    print("🧪 Testing database setup...")
    
    try:
        from app import app
        from extensions import db
        from models import User, Product, Category
        
        with app.app_context():
            # Test database connection
            user_count = User.query.count()
            product_count = Product.query.count()
            category_count = Category.query.count()
            
            print(f"✅ Database connected successfully")
            print(f"   Users: {user_count}")
            print(f"   Products: {product_count}")
            print(f"   Categories: {category_count}")
            
            if user_count >= 2 and product_count >= 10 and category_count >= 5:
                print("✅ Sample data loaded correctly")
                return True
            else:
                print("❌ Insufficient sample data")
                return False
                
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_flask_app():
    """Test Flask application startup."""
    print("\n🧪 Testing Flask application...")
    
    try:
        # Start Flask app in background
        process = subprocess.Popen(
            ['python', 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.getcwd()
        )
        
        # Wait for app to start
        time.sleep(3)
        
        # Test if app is running
        try:
            response = requests.get('http://localhost:5000', timeout=5)
            if response.status_code == 200:
                print("✅ Flask application started successfully")
                print("✅ Home page accessible")
                
                # Test other endpoints
                endpoints_to_test = [
                    ('/products', 'Products page'),
                    ('/login', 'Login page'),
                    ('/register', 'Registration page')
                ]
                
                for endpoint, description in endpoints_to_test:
                    try:
                        resp = requests.get(f'http://localhost:5000{endpoint}', timeout=5)
                        if resp.status_code == 200:
                            print(f"✅ {description} accessible")
                        else:
                            print(f"⚠️  {description} returned status {resp.status_code}")
                    except Exception as e:
                        print(f"❌ {description} failed: {e}")
                
                # Terminate the process
                process.terminate()
                process.wait()
                return True
            else:
                print(f"❌ Flask app returned status {response.status_code}")
                process.terminate()
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Could not connect to Flask app: {e}")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def test_database_utilities():
    """Test database utility functions."""
    print("\n🧪 Testing database utilities...")
    
    try:
        # Test database stats
        result = subprocess.run(['python', 'database.py', 'stats'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Database stats utility works")
        else:
            print(f"❌ Database stats failed: {result.stderr}")
            return False
        
        # Test SQLite browser
        result = subprocess.run(['python', 'sqlite_browser.py', 'tables'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ SQLite browser works")
        else:
            print(f"❌ SQLite browser failed: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Database utilities test failed: {e}")
        return False

def test_imports():
    """Test that all modules can be imported."""
    print("\n🧪 Testing module imports...")
    
    modules_to_test = [
        'app',
        'models',
        'routes',
        'extensions',
        'database',
        'setup_database'
    ]
    
    all_passed = True
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module} imports successfully")
        except Exception as e:
            print(f"❌ {module} import failed: {e}")
            all_passed = False
    
    return all_passed

def run_all_tests():
    """Run all tests and provide summary."""
    print("🚀 E-Commerce Platform - Automated Test Suite")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Database Setup", test_database_setup),
        ("Database Utilities", test_database_utilities),
        ("Flask Application", test_flask_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} tests...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The application is ready to use.")
        print("\n🚀 To start the application manually:")
        print("   python app.py")
        print("\n🌐 Then visit: http://localhost:5000")
        print("\n👤 Test accounts:")
        print("   Admin: admin / admin123")
        print("   User:  testuser / test123")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the errors above.")
        return False
    
    return True

if __name__ == '__main__':
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Virtual environment not detected.")
        print("Please activate the virtual environment first:")
        print("   source venv/bin/activate")
        sys.exit(1)
    
    # Run tests
    success = run_all_tests()
    sys.exit(0 if success else 1)
