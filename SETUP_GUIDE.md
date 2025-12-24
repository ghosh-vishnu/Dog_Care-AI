# Project Setup Guide

## Project Structure

```
Dog_AI/
├── backend/          # Django Backend
├── frontend/          # React Frontend
└── README.md         # Main documentation
```

## Backend Setup (Django)

### Step 1: Navigate to Backend

```bash
cd backend
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Create .env File

Create `.env` file in `backend/` directory:

```env
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
DB_NAME=pet_health_db
DB_USER=postgres
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432
```

### Step 6: Run Migrations

```bash
python manage.py migrate
```

### Step 7: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 8: Run Server

```bash
python manage.py runserver
```

Backend will run at: **http://127.0.0.1:8000/**

---

## Frontend Setup (React)

### Step 1: Navigate to Frontend

```bash
cd frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Create .env File (Optional)

Create `.env` file in `frontend/` directory:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

### Step 4: Run Development Server

```bash
npm run dev
```

Frontend will run at: **http://localhost:5173/**

---

## Quick Commands

### Backend Commands

```bash
cd backend
python manage.py runserver          # Start server
python manage.py makemigrations     # Create migrations
python manage.py migrate            # Apply migrations
python manage.py createsuperuser    # Create admin
python manage.py check              # Check for errors
```

### Frontend Commands

```bash
cd frontend
npm run dev      # Development server
npm run build    # Production build
npm run preview  # Preview build
```

---

## Access Points

- **Backend API:** http://127.0.0.1:8000/api/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Frontend:** http://localhost:5173/

---

## Troubleshooting

### Backend Issues

1. **Module not found:** Make sure virtual environment is activated
2. **Database error:** Check PostgreSQL is running and .env is correct
3. **Port already in use:** Change port with `python manage.py runserver 8001`

### Frontend Issues

1. **npm install fails:** Try `npm cache clean --force`
2. **API connection fails:** Check backend is running and CORS is configured
3. **Port already in use:** Vite will automatically use next available port

---

## Next Steps

1. Read [API_ENDPOINTS.md](./API_ENDPOINTS.md) for API documentation
2. Read [API_RESPONSE_STANDARD.md](./API_RESPONSE_STANDARD.md) for response format
3. Check [PHASE1_AUDIT_REPORT.md](./PHASE1_AUDIT_REPORT.md) for features

