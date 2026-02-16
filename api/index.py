"""
Vercel Entry Point
This file is required by Vercel to run the FastAPI application
"""
import sys
from pathlib import Path

# Add parent directory to path so we can import from app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app

# Vercel will automatically use this app object
# Do NOT add uvicorn.run() here
