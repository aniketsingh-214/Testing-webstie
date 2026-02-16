# FastAPI Defacement Test - Government Portal

A production-ready government portal built with FastAPI for defacement testing purposes.

## 🚀 Features

- **Dynamic Routes**: Home, Departments, Services, and Contact pages
- **Modern UI**: Gradient backgrounds, animations, and responsive design
- **API Endpoints**: RESTful API for departments, services, and contact forms
- **Production Ready**: CORS, security headers, logging, and error handling
- **Form Validation**: Client and server-side validation
- **Mock Database**: 6 departments and 14 government services
- **Defacement Monitoring**: Hash-based monitoring system

## 📋 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
```

The application will be available at: **http://localhost:9000**

## 🌐 Pages

- **Home** (`/`) - Hero section with featured departments and services
- **Departments** (`/departments`) - Browse all government departments
- **Services** (`/services`) - Explore government services with filtering
- **Contact** (`/contact`) - Contact form with validation

## 🔌 API Endpoints

- `GET /health` - Health check
- `GET /api/departments` - List all departments
- `GET /api/services` - List services (with optional filters)
- `POST /api/contact` - Submit contact form
- `GET /api/stats` - Portal statistics

## 🎨 Tech Stack

- **Backend**: FastAPI, Pydantic, Uvicorn
- **Frontend**: Jinja2 Templates, Vanilla CSS, JavaScript
- **Features**: CORS, Security Headers, Logging, Form Validation

## 📁 Project Structure

```
app/
├── main.py              # Main application
├── config.py            # Configuration
├── models.py            # Data models
├── database.py          # Mock database
├── middleware/          # Security middleware
├── routes/              # API and page routes
├── static/              # CSS and JavaScript
└── templates/           # HTML templates
```

## 🔧 Configuration

Copy `.env.example` to `.env` and customize settings:

```env
ENVIRONMENT=development
DEBUG=True
PORT=9000
```

## 📝 License

This is a testing environment for defacement detection.

## 🤝 Contributing

This is a demonstration project for defacement testing purposes.
