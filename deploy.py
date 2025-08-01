#!/usr/bin/env python3
"""
Complete deployment script for the e-commerce platform.
This script sets up everything needed to run the application.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python():
    """Check Python version."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} is too old. Need Python 3.8+")
        return False

def setup_virtual_environment():
    """Set up virtual environment."""
    if os.path.exists('venv'):
        print("📁 Virtual environment already exists")
        return True
    
    return run_command('python3 -m venv venv', 'Creating virtual environment')

def install_dependencies():
    """Install Python dependencies."""
    activate_cmd = 'source venv/bin/activate' if os.name != 'nt' else 'venv\\Scripts\\activate'
    return run_command(f'{activate_cmd} && pip install -r requirements.txt', 'Installing dependencies')

def setup_environment_file():
    """Set up environment file."""
    if os.path.exists('.env'):
        print("📄 Environment file already exists")
        return True
    
    if os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        print("✅ Environment file created from template")
        print("⚠️  Please edit .env file with your Stripe keys for payment processing")
        return True
    else:
        # Create basic .env file
        env_content = """# Flask Configuration
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///ecommerce.db

# Stripe Configuration (Get real keys from https://stripe.com)
STRIPE_PUBLISHABLE_KEY=pk_test_dummy_key
STRIPE_SECRET_KEY=sk_test_dummy_key
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Basic environment file created")
        return True

def initialize_database():
    """Initialize database with sample data."""
    activate_cmd = 'source venv/bin/activate' if os.name != 'nt' else 'venv\\Scripts\\activate'
    return run_command(f'{activate_cmd} && python setup_database.py', 'Initializing database')

def test_application():
    """Test the application."""
    activate_cmd = 'source venv/bin/activate' if os.name != 'nt' else 'venv\\Scripts\\activate'
    return run_command(f'{activate_cmd} && python test_routes.py', 'Testing application')

def create_directories():
    """Create necessary directories."""
    directories = ['static/uploads', 'backups', 'instance']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Created necessary directories")
    return True

def display_summary():
    """Display deployment summary."""
    print("\n" + "="*60)
    print("🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n🚀 To start the application:")
    
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("   python app.py")
    print("\n🌐 Then visit: http://localhost:5000")
    print("\n👤 Test accounts:")
    print("   Admin: admin / admin123")
    print("   User:  testuser / test123")
    print("\n📊 Sample data includes:")
    print("   • 2 users (admin + customer)")
    print("   • 6 product categories")
    print("   • 19 sample products")
    print("\n🛠️  Database tools:")
    print("   python database.py stats     # View statistics")
    print("   python sqlite_browser.py     # Browse database")
    print("   python demo_sqlite.py        # SQLite demo")
    print("\n📚 Documentation:")
    print("   • README.md - General information")
    print("   • TESTING_GUIDE.md - Testing instructions")
    print("   • SQLITE_INTEGRATION.md - Database details")
    print("   • RUN_INSTRUCTIONS.md - Running guide")

def main():
    """Main deployment function."""
    print("🛍️  E-Commerce Platform Deployment")
    print("="*60)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    steps = [
        ("Python Version Check", check_python),
        ("Virtual Environment Setup", setup_virtual_environment),
        ("Dependencies Installation", install_dependencies),
        ("Environment Configuration", setup_environment_file),
        ("Directory Creation", create_directories),
        ("Database Initialization", initialize_database),
        ("Application Testing", test_application),
    ]
    
    failed_steps = []
    
    for step_name, step_function in steps:
        print(f"\n📋 Step: {step_name}")
        if not step_function():
            failed_steps.append(step_name)
    
    if failed_steps:
        print(f"\n❌ Deployment failed. Failed steps: {', '.join(failed_steps)}")
        print("Please check the errors above and try again.")
        return False
    else:
        display_summary()
        return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
