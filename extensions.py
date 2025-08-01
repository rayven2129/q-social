"""
Extensions initialization for the Flask application.
This module helps avoid circular imports.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
