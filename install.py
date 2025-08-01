#!/usr/bin/env python3
"""
Installation script for Python 3.13 compatibility
Handles problematic packages gracefully
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors gracefully"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} successful")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def install_package(package, description=None):
    """Install a single package"""
    if description is None:
        description = f"Installing {package}"
    
    return run_command(f"pip install {package}", description)

def main():
    """Main installation process"""
    print("🚀 Installing E-Commerce Platform Dependencies for Python 3.13\n")
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: You don't appear to be in a virtual environment.")
        print("   It's recommended to create one with: python3 -m venv venv && source venv/bin/activate")
        response = input("   Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Installation cancelled.")
            return False
    
    # Upgrade pip first
    print("🔧 Upgrading pip...")
    run_command("pip install --upgrade pip", "Upgrading pip")
    
    # Core packages that should work
    core_packages = [
        ("Flask>=3.0.0", "Flask web framework"),
        ("Werkzeug>=3.0.0", "WSGI utilities"),
        ("python-dotenv>=1.0.0", "Environment variables"),
        ("flask-cors>=4.0.0", "CORS support"),
        ("tabulate>=0.9.0", "Table formatting"),
    ]
    
    # Database packages
    db_packages = [
        ("Flask-SQLAlchemy>=3.1.0", "SQLAlchemy integration"),
    ]
    
    # Authentication packages
    auth_packages = [
        ("Flask-Login>=0.6.0", "User session management"),
        ("Flask-WTF>=1.2.0", "Form handling"),
        ("WTForms>=3.1.0", "Form validation"),
        ("bcrypt>=4.1.0", "Password hashing"),
        ("email-validator>=2.1.0", "Email validation"),
    ]
    
    # Payment packages
    payment_packages = [
        ("stripe>=8.0.0", "Stripe payment processing"),
    ]
    
    # Optional packages (may fail on Python 3.13)
    optional_packages = [
        ("Pillow>=10.0.0", "Image processing (optional)"),
    ]
    
    success_count = 0
    total_count = 0
    
    # Install core packages
    print("\n📦 Installing core packages...")
    for package, description in core_packages:
        total_count += 1
        if install_package(package, description):
            success_count += 1
    
    # Install database packages
    print("\n🗄️  Installing database packages...")
    for package, description in db_packages:
        total_count += 1
        if install_package(package, description):
            success_count += 1
    
    # Install authentication packages
    print("\n🔐 Installing authentication packages...")
    for package, description in auth_packages:
        total_count += 1
        if install_package(package, description):
            success_count += 1
    
    # Install payment packages
    print("\n💳 Installing payment packages...")
    for package, description in payment_packages:
        total_count += 1
        if install_package(package, description):
            success_count += 1
    
    # Install optional packages
    print("\n🎨 Installing optional packages...")
    for package, description in optional_packages:
        total_count += 1
        print(f"📦 {description}...")
        if install_package(package, description):
            success_count += 1
        else:
            print(f"⚠️  {description} failed - continuing without it (not critical for API)")
    
    # Summary
    print(f"\n📊 Installation Summary:")
    print(f"   ✅ Successful: {success_count}/{total_count}")
    print(f"   ❌ Failed: {total_count - success_count}/{total_count}")
    
    if success_count >= total_count - 1:  # Allow 1 failure (likely Pillow)
        print("\n🎉 Installation completed successfully!")
        print("\nNext steps:")
        print("1. Set up your .env file with Stripe keys")
        print("2. Run: python setup_database.py")
        print("3. Run: python app.py")
        print("4. Visit: http://localhost:5000")
        return True
    else:
        print("\n❌ Too many packages failed to install.")
        print("Please check the errors above and try installing manually.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
