"""
Initialize routes blueprints
"""
from .auth import auth_bp
from .admin import admin_bp
from .citizen import citizen_bp
from .volunteer import volunteer_bp
from .api import api_bp

__all__ = ['auth_bp', 'admin_bp', 'citizen_bp', 'volunteer_bp', 'api_bp']
