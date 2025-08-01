#!/usr/bin/env python3
"""
Simple startup script for the e-commerce platform.
"""

import os
import sys
import subprocess

def main():
    print("🛍️  E-Commerce Platform Startup")
    print("="*50)
    
    # Check if we're in virtual environment
    if not (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
        print("⚠️  Virtual environment not detected.")
        print("Please run:")
        print("  python3 -m venv venv")
        print("  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("  pip install -r requirements.txt")
        print("  python3 start.py")
        return False
    
    # Check if database exists
    if not os.path.exists('instance/ecommerce.db') and not os.path.exists('ecommerce.db'):
        print("📊 Database not found. Initializing...")
        try:
            from setup_database import setup_database
            setup_database()
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            return False
    
    # Start the application
    print("🚀 Starting application...")
    try:
        from app import app
        print("✅ Application loaded successfully!")
        print("🌐 Starting server at http://localhost:5000")
        print("👤 Test accounts: admin/admin123, testuser/test123")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        return False
    
    return True

if __name__ == '__main__':
    main()
