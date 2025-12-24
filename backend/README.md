# Pet Health Backend

Django + Django REST Framework backend for Pet Health Mobile Application.

## Project Structure

```
backend/
├── apps/              # Django applications
│   ├── accounts/      # User management
│   ├── pets/          # Pet management
│   ├── health/         # Health records & vaccinations
│   ├── subscriptions/  # Subscription plans
│   ├── appointments/   # Appointment scheduling
│   └── notifications/  # User notifications
├── config/            # Django project settings
│   └── settings/      # Environment-based settings
├── utils/             # Utility modules (responses, exceptions)
├── manage.py          # Django management script
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (create from .env.example)
└── README.md         # This file
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

**Important:** Create a `.env` file in the `backend/` directory (not in root):

```bash
# Copy example file
cp .env.example .env
```

Or create `.env` manually in `backend/` directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=pet_health_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

**Note:** `.env` file should be in `backend/` directory, not in root!

### 5. Database Setup

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Server will run at `http://127.0.0.1:8000/`

## API Documentation

- API Endpoints: See `../API_ENDPOINTS.md`
- Response Standard: See `../API_RESPONSE_STANDARD.md`
- Testing Guide: See `../API_TESTING_GUIDE.md`

## Admin Panel

Access Django Admin at: `http://127.0.0.1:8000/admin/`

## Key Features

- ✅ JWT Authentication
- ✅ Role-based Access Control (Admin/User)
- ✅ Custom User Model
- ✅ Soft Delete Support
- ✅ Standardized API Responses
- ✅ Custom Exception Handling
- ✅ Production-ready Security

## Tech Stack

- Python 3.12+
- Django 4.2+
- Django REST Framework
- PostgreSQL
- JWT Authentication

## Important Notes

- **`.env` file location:** Must be in `backend/` directory
- **Working directory:** Run all Django commands from `backend/` directory
- **Virtual environment:** Can be in root or backend/ (your choice)
