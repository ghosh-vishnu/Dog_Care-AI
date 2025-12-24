# Pet Health Mobile Application

Complete full-stack application for managing pet health records, vaccinations, appointments, and subscriptions.

## Project Structure

```
Dog_AI/
├── backend/           # Django REST Framework Backend
│   ├── apps/         # Django applications
│   ├── config/        # Project settings
│   ├── utils/         # Utility modules
│   └── manage.py      # Django management
├── frontend/          # React + Vite Frontend
│   ├── src/           # React source code
│   └── package.json   # Frontend dependencies
└── README.md          # This file
```

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend runs at: `http://127.0.0.1:8000/`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:5173/`

## Documentation

- [API Endpoints](./API_ENDPOINTS.md) - Complete API documentation
- [API Response Standard](./API_RESPONSE_STANDARD.md) - Response format guide
- [Phase-1 Audit Report](./PHASE1_AUDIT_REPORT.md) - Production readiness audit
- [Backend README](./backend/README.md) - Backend setup details
- [Frontend README](./frontend/README.md) - Frontend setup details

## Features

### Phase-1 (Completed) ✅

- ✅ User Authentication (JWT)
- ✅ User Profile Management
- ✅ Pet Management (CRUD)
- ✅ Health Records & Vaccinations
- ✅ Appointment Scheduling
- ✅ Subscription Plans
- ✅ Notifications
- ✅ Admin Panel
- ✅ Security & Permissions
- ✅ Standardized API Responses

## Tech Stack

### Backend
- Python 3.12+
- Django 4.2+
- Django REST Framework
- PostgreSQL
- JWT Authentication

### Frontend
- React 18+
- Vite
- React Router DOM
- Axios
- Context API

## Development

### Backend Commands

```bash
cd backend
python manage.py runserver          # Run development server
python manage.py makemigrations     # Create migrations
python manage.py migrate            # Apply migrations
python manage.py createsuperuser    # Create admin user
python manage.py check              # Check for issues
```

### Frontend Commands

```bash
cd frontend
npm run dev      # Development server
npm run build    # Production build
npm run preview  # Preview production build
```

## Environment Variables

### Backend (.env in backend/)

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=pet_health_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### Frontend (.env in frontend/)

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## API Base URL

Default: `http://127.0.0.1:8000/api`

## Admin Panel

URL: `http://127.0.0.1:8000/admin/`

## License

Private Project

## Contact

For questions or issues, please contact the development team.
