"""
Vercel ASGI entry point for FastAPI backend
"""
import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import the FastAPI app
from app.main import app

# For Vercel ASGI deployment
handler = app
