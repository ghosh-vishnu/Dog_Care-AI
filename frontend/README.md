# Pet Health Frontend

React frontend application for Pet Health Mobile Application with Signup and Login functionality.

## Features

- ✅ User Registration (Signup)
- ✅ User Login
- ✅ Protected Routes
- ✅ Token-based Authentication
- ✅ Beautiful UI with modern design
- ✅ Form Validation
- ✅ Error Handling
- ✅ Responsive Design

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable components
│   │   └── ProtectedRoute.jsx
│   ├── context/          # React Context (Auth)
│   │   └── AuthContext.jsx
│   ├── pages/           # Page components
│   │   ├── Signup.jsx
│   │   ├── Login.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Auth.css
│   │   └── Dashboard.css
│   ├── services/        # API services
│   │   └── api.js
│   ├── App.jsx          # Main App component
│   ├── App.css
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

## API Endpoints Used

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/auth/users/me/` - Get current user profile

## Usage

### Signup Flow

1. Navigate to `/signup`
2. Fill in the registration form:
   - First Name (required)
   - Last Name (required)
   - Email (required)
   - Phone Number (optional)
   - Password (required, min 8 characters)
   - Confirm Password (required)
3. Click "Sign Up"
4. On success, automatically redirected to Dashboard

### Login Flow

1. Navigate to `/login`
2. Enter email and password
3. Click "Sign In"
4. On success, redirected to Dashboard

### Dashboard

- Shows user information
- Logout functionality
- Protected route (requires authentication)

## Environment

Make sure your Django backend is running at:
```
http://127.0.0.1:8000
```

## Build for Production

```bash
npm run build
```

The build files will be in the `dist/` directory.

## Technologies Used

- React 18
- React Router DOM
- Axios (HTTP client)
- Vite (Build tool)
- CSS3 (Modern styling)

## Notes

- Tokens are stored in `localStorage`
- Automatic token refresh on 401 errors
- Form validation on both client and server side
- Responsive design for mobile and desktop


