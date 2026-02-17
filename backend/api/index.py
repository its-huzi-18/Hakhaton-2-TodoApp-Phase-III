"""
Vercel serverless function entry point for FastAPI backend.
This file must be in the api/ directory for Vercel Python runtime.
"""
import sys
import os

# Add parent directory to path so we can import from app/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the FastAPI app from app.main
from app.main import app

# Vercel expects the handler to be the ASGI app itself
handler = app
