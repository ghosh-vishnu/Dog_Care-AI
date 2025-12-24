# Pet Health Frontend

React + Vite frontend for Pet Health Mobile Application.

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable components
│   ├── context/       # React Context (Auth)
│   ├── pages/         # Page components
│   ├── services/      # API services
│   ├── App.jsx        # Main app component
│   └── main.jsx       # Entry point
├── package.json       # Dependencies
└── vite.config.js     # Vite configuration
```

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Configuration

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

### 3. Run Development Server

```bash
npm run dev
```

Frontend will run at `http://localhost:5173/`

### 4. Build for Production

```bash
npm run build
```

## Features

- ✅ User Registration
- ✅ User Login
- ✅ JWT Token Management
- ✅ Protected Routes
- ✅ API Integration
- ✅ Responsive Design

## Tech Stack

- React 18+
- Vite
- React Router DOM
- Axios
- Context API

## API Integration

The frontend connects to the Django backend API. Make sure the backend is running before starting the frontend.

Default API URL: `http://127.0.0.1:8000/api`
