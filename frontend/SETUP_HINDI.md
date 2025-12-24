# Frontend Setup Guide (हिंदी में)

## 🚀 Quick Start

### Step 1: Dependencies Install करें

```bash
cd frontend
npm install
```

**Note:** पहली बार में 2-3 मिनट लग सकते हैं

### Step 2: Development Server Start करें

```bash
npm run dev
```

**Output:**
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### Step 3: Browser में खोलें

```
http://localhost:3000
```

---

## 📋 Features

### ✅ Signup Page (`/signup`)
- First Name, Last Name
- Email
- Phone Number (optional)
- Password & Confirm Password
- Form Validation
- Error Handling
- Success Message

### ✅ Login Page (`/login`)
- Email & Password
- Form Validation
- Error Handling
- Auto redirect to Dashboard

### ✅ Dashboard (`/dashboard`)
- User Information Display
- Logout Button
- Protected Route (login required)

---

## 🎯 Testing Flow

### 1. Signup करें:
1. Browser में `http://localhost:3000` खोलें
2. Automatically `/login` page पर redirect होगा
3. "Sign Up" link पर click करें
4. Form भरें और "Sign Up" button click करें
5. Success होने पर Dashboard पर redirect होगा

### 2. Login करें:
1. `/login` page पर जाएं
2. Email और Password enter करें
3. "Sign In" button click करें
4. Dashboard पर redirect होगा

### 3. Dashboard देखें:
- User की सारी information दिखेगी
- Logout button से logout कर सकते हैं

---

## 🔧 Important Points

### Backend Connection:
- Frontend automatically `http://127.0.0.1:8000` पर connect करेगा
- **Django server running होना चाहिए!**

### Token Storage:
- Login/Signup के बाद tokens `localStorage` में save होते हैं
- Automatic token refresh होता है

### Routes:
- `/` → Auto redirect to `/login`
- `/login` → Login page
- `/signup` → Signup page
- `/dashboard` → Dashboard (protected)

---

## 🐛 Troubleshooting

### Error: "Cannot find module"
```bash
npm install
```

### Error: "Port 3000 already in use"
```bash
# Another terminal में:
# Port change करने के लिए vite.config.js में port change करें
```

### Backend Connection Error:
- Django server running है? (`python manage.py runserver`)
- CORS settings check करें
- Backend URL correct है? (`http://127.0.0.1:8000`)

---

## 📁 File Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── Signup.jsx      # Signup page
│   │   ├── Login.jsx       # Login page
│   │   ├── Dashboard.jsx  # Dashboard page
│   │   └── Auth.css       # Auth pages styling
│   ├── components/
│   │   └── ProtectedRoute.jsx  # Route protection
│   ├── context/
│   │   └── AuthContext.jsx     # Authentication state
│   ├── services/
│   │   └── api.js              # API calls
│   └── App.jsx                  # Main app
├── package.json
└── vite.config.js
```

---

## 🎨 UI Features

- Modern gradient background
- Clean card design
- Form validation with error messages
- Loading states
- Success/Error notifications
- Responsive design (mobile friendly)
- Smooth animations

---

## ✅ Next Steps

1. **Install dependencies:** `npm install`
2. **Start server:** `npm run dev`
3. **Open browser:** `http://localhost:3000`
4. **Test Signup/Login**

**Happy Coding! 🎉**

