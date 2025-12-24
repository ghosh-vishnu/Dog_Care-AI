# Pet Health Backend

Production-ready Django + Django REST Framework backend for Pet Health Mobile Application.

## Project Structure

```
Dog_AI/
├── config/                 # Main project configuration
│   ├── settings/          # Environment-based settings
│   │   ├── base.py        # Base settings (common across all environments)
│   │   └── local.py       # Local development settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── apps/                   # Django applications
│   ├── accounts/          # User accounts and authentication
│   ├── pets/              # Pet management
│   ├── health/            # Health records, vaccinations, medications
│   ├── appointments/      # Appointment scheduling
│   └── notifications/     # User notifications
├── static/                # Static files
├── media/                 # Media files (user uploads)
├── logs/                  # Application logs
├── templates/             # Django templates
├── manage.py              # Django management script
├── requirements.txt      # Python dependencies
├── env.example           # Environment variables template
└── .gitignore            # Git ignore rules
```

## Features

- **Environment-based Configuration**: Separate settings for different environments
- **PostgreSQL Database**: Production-ready database configuration
- **Django REST Framework**: Full REST API support
- **Custom User Model**: Extended user model with additional fields
- **CORS Support**: Configured for frontend integration
- **Admin Panel**: Django admin interface for all models
- **Scalable Architecture**: Modular app structure for easy expansion

## Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip (Python package manager)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Dog_AI
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL Database

Create a PostgreSQL database:

```sql
CREATE DATABASE pet_health_db;
CREATE USER postgres WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE pet_health_db TO postgres;
```

### 5. Configure Environment Variables

Copy the example environment file:

```bash
# On Windows
copy env.example .env

# On macOS/Linux
cp env.example .env
```

Edit `.env` file with your configuration:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=pet_health_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

TIME_ZONE=UTC
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

The server will be available at `http://127.0.0.1:8000/`

## API Endpoints

- Admin Panel: `http://127.0.0.1:8000/admin/`
- API Auth: `http://127.0.0.1:8000/api/auth/`
- API Pets: `http://127.0.0.1:8000/api/pets/`
- API Health: `http://127.0.0.1:8000/api/health/`
- API Appointments: `http://127.0.0.1:8000/api/appointments/`
- API Notifications: `http://127.0.0.1:8000/api/notifications/`

## API Testing Guide

For detailed Postman testing instructions, request/response examples, and step-by-step testing guide, see **[API_TESTING_GUIDE.md](./API_TESTING_GUIDE.md)**

The guide includes:
- Complete API endpoint documentation
- Request/Response examples
- Postman collection setup
- Authentication flow
- Error handling examples
- Testing scenarios

## Applications Overview

### Accounts App
- Custom User model with extended fields
- User authentication and authorization
- Profile management

### Pets App
- Pet registration and management
- Pet profiles with photos
- Breed and type tracking

### Health App
- Health records management
- Vaccination tracking
- Medication records
- Health history

### Appointments App
- Appointment scheduling
- Veterinarian assignment
- Appointment status tracking

### Notifications App
- User notifications
- Notification types (appointments, vaccinations, etc.)
- Read/unread status

## Development

### Running Tests

```bash
python manage.py test
```

### Collecting Static Files

```bash
python manage.py collectstatic
```

### Creating New Migrations

```bash
python manage.py makemigrations <app_name>
python manage.py migrate
```

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in production settings
2. Configure proper `ALLOWED_HOSTS`
3. Use a production-ready database
4. Set up proper static file serving
5. Configure SSL/HTTPS
6. Set up proper logging
7. Use environment variables for sensitive data

## License

Venturing Digitally Pvt Ltd.

## Author

Vishnu Kumar Ghosh
