"""
Vercel Entry Point
This file is required by Vercel to run the FastAPI application
"""
from app.main import app

# Vercel will automatically use this app object
# Do NOT add uvicorn.run() here
