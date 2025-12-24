# API Testing Guide - Postman

Complete guide for testing all Pet Health Backend APIs using Postman.

## Table of Contents
1. [Setup](#setup)
2. [Authentication Flow](#authentication-flow)
3. [API Endpoints](#api-endpoints)
4. [Postman Collection Setup](#postman-collection-setup)
5. [Testing Examples](#testing-examples)

---

## Setup

### Base URL
```
http://127.0.0.1:8000
```

### Required Headers
For authenticated requests, include:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## Authentication Flow

### 1. User Registration

**Endpoint:** `POST /api/auth/register/`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "email": "abc@gmail.com",
    "password": "abc@1234",
    "password_confirm": "abc@1234",
    "first_name": "Satyam",
    "last_name": "Doe",
    "phone_number": "7292992274",
    "role": "USER"
}
```

**Response (201 Created):**
```json
{
    "message": "User registered successfully.",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "phone_number": "+1234567890",
        "profile_picture": null,
        "role": "USER",
        "is_veterinarian": false,
        "is_active": true,
        "is_admin": false,
        "is_regular_user": true,
        "date_joined": "2024-01-15T10:30:00Z",
        "last_login": null
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

**Note:** Save the `access` and `refresh` tokens for subsequent requests.

---

### 2. User Login

**Endpoint:** `POST /api/auth/login/`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
    "message": "Login successful.",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "phone_number": "+1234567890",
        "role": "USER",
        "is_veterinarian": false,
        "is_active": true,
        "is_admin": false,
        "is_regular_user": true,
        "date_joined": "2024-01-15T10:30:00Z",
        "last_login": "2024-01-15T11:00:00Z"
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

---

### 3. Get JWT Token (Alternative)

**Endpoint:** `POST /api/auth/token/`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "phone_number": "+1234567890",
        "role": "USER",
        "is_veterinarian": false,
        "is_active": true,
        "is_admin": false,
        "is_regular_user": true,
        "date_joined": "2024-01-15T10:30:00Z",
        "last_login": "2024-01-15T11:00:00Z"
    }
}
```

---

### 4. Refresh JWT Token

**Endpoint:** `POST /api/auth/token/refresh/`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 5. Verify JWT Token

**Endpoint:** `POST /api/auth/token/verify/`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{}
```

**Response (401 Unauthorized) - Invalid Token:**
```json
{
    "detail": "Token is invalid or expired"
}
```

---

## User Management APIs

### 6. Get Current User Profile

**Endpoint:** `GET /api/auth/users/me/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "phone_number": "+1234567890",
    "profile_picture": null,
    "role": "USER",
    "is_veterinarian": false,
    "is_active": true,
    "is_admin": false,
    "is_regular_user": true,
    "date_joined": "2024-01-15T10:30:00Z",
    "last_login": "2024-01-15T11:00:00Z"
}
```

---

### 7. Update Current User Profile

**Endpoint:** `PUT /api/auth/users/me/` or `PATCH /api/auth/users/me/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body (PUT - Full Update):**
```json
{
    "first_name": "Jane",
    "last_name": "Smith",
    "phone_number": "+9876543210",
    "is_veterinarian": true
}
```

**Request Body (PATCH - Partial Update):**
```json
{
    "first_name": "Jane"
}
```

**Response (200 OK):**
```json
{
    "message": "Profile updated successfully.",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "full_name": "Jane Smith",
        "phone_number": "+9876543210",
        "role": "USER",
        "is_veterinarian": true,
        "is_active": true,
        "is_admin": false,
        "is_regular_user": true,
        "date_joined": "2024-01-15T10:30:00Z",
        "last_login": "2024-01-15T11:00:00Z"
    }
}
```

---

### 8. Change Password

**Endpoint:** `POST /api/auth/users/change-password/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "old_password": "SecurePass123!",
    "new_password": "NewSecurePass456!",
    "new_password_confirm": "NewSecurePass456!"
}
```

**Response (200 OK):**
```json
{
    "message": "Password changed successfully."
}
```

**Error Response (400 Bad Request):**
```json
{
    "old_password": ["Old password is incorrect."]
}
```

or

```json
{
    "new_password_confirm": ["New passwords do not match."]
}
```

---

### 9. List All Users (Admin Only)

**Endpoint:** `GET /api/auth/users/`

**Headers:**
```
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "count": 10,
    "next": "http://127.0.0.1:8000/api/auth/users/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "email": "user@example.com",
            "full_name": "John Doe",
            "role": "USER",
            "is_veterinarian": false,
            "is_active": true,
            "date_joined": "2024-01-15T10:30:00Z"
        },
        {
            "id": 2,
            "email": "admin@example.com",
            "full_name": "Admin User",
            "role": "ADMIN",
            "is_veterinarian": false,
            "is_active": true,
            "date_joined": "2024-01-14T09:00:00Z"
        }
    ]
}
```

---

### 10. Get User by ID (Admin or Owner)

**Endpoint:** `GET /api/auth/users/{id}/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "phone_number": "+1234567890",
    "profile_picture": null,
    "role": "USER",
    "is_veterinarian": false,
    "is_active": true,
    "is_admin": false,
    "is_regular_user": true,
    "date_joined": "2024-01-15T10:30:00Z",
    "last_login": "2024-01-15T11:00:00Z"
}
```

---

### 11. Update User (Admin or Owner)

**Endpoint:** `PUT /api/auth/users/{id}/` or `PATCH /api/auth/users/{id}/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "first_name": "Updated",
    "last_name": "Name",
    "phone_number": "+1111111111",
    "is_veterinarian": false
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "email": "user@example.com",
    "first_name": "Updated",
    "last_name": "Name",
    "full_name": "Updated Name",
    "phone_number": "+1111111111",
    "role": "USER",
    "is_veterinarian": false,
    "is_active": true,
    "is_admin": false,
    "is_regular_user": true,
    "date_joined": "2024-01-15T10:30:00Z",
    "last_login": "2024-01-15T11:00:00Z"
}
```

---

### 12. Delete User (Admin Only - Soft Delete)

**Endpoint:** `DELETE /api/auth/users/{id}/`

**Headers:**
```
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "message": "User deactivated successfully."
}
```

**Note:** This deactivates the user (sets `is_active=False`) instead of deleting from database.

---

## Postman Collection Setup

### Step 1: Create Environment Variables

1. Click on **Environments** in Postman
2. Create a new environment named "Pet Health API"
3. Add these variables:

| Variable | Initial Value | Current Value |
|----------|---------------|---------------|
| `base_url` | http://127.0.0.1:8000 | http://127.0.0.1:8000 |
| `access_token` | (leave empty) | (will be set automatically) |
| `refresh_token` | (leave empty) | (will be set automatically) |
| `user_id` | (leave empty) | (will be set automatically) |

### Step 2: Setup Authorization

For authenticated requests:

1. Go to **Authorization** tab
2. Select **Type: Bearer Token**
3. Enter `{{access_token}}` in the Token field

### Step 3: Auto-save Tokens (Using Tests Script)

Add this script to **Tests** tab in Login/Register requests:

```javascript
// Save access token
if (pm.response.code === 200 || pm.response.code === 201) {
    var jsonData = pm.response.json();
    if (jsonData.tokens) {
        pm.environment.set("access_token", jsonData.tokens.access);
        pm.environment.set("refresh_token", jsonData.tokens.refresh);
    }
    if (jsonData.user) {
        pm.environment.set("user_id", jsonData.user.id);
    }
}
```

---

## Testing Examples

### Example 1: Complete User Flow

1. **Register a new user:**
   - Method: `POST`
   - URL: `{{base_url}}/api/auth/register/`
   - Body: Registration JSON
   - Save tokens from response

2. **Get user profile:**
   - Method: `GET`
   - URL: `{{base_url}}/api/auth/users/me/`
   - Authorization: Bearer Token (auto-filled)

3. **Update profile:**
   - Method: `PATCH`
   - URL: `{{base_url}}/api/auth/users/me/`
   - Body: Update JSON
   - Authorization: Bearer Token

4. **Change password:**
   - Method: `POST`
   - URL: `{{base_url}}/api/auth/users/change-password/`
   - Body: Password change JSON
   - Authorization: Bearer Token

### Example 2: Token Management

1. **Login:**
   - Method: `POST`
   - URL: `{{base_url}}/api/auth/login/`
   - Body: Login credentials
   - Save tokens

2. **Verify token:**
   - Method: `POST`
   - URL: `{{base_url}}/api/auth/token/verify/`
   - Body: `{"token": "{{access_token}}"}`

3. **Refresh token (when expired):**
   - Method: `POST`
   - URL: `{{base_url}}/api/auth/token/refresh/`
   - Body: `{"refresh": "{{refresh_token}}"}`

---

## Error Responses

### 400 Bad Request
```json
{
    "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

or

```json
{
    "detail": "Given token not valid for any token type"
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
    "detail": "A server error occurred."
}
```

---

## Common Testing Scenarios

### Scenario 1: New User Registration and Login
1. Register with valid data
2. Verify email uniqueness (try duplicate email)
3. Verify password match (mismatched passwords)
4. Login with registered credentials
5. Get profile with token

### Scenario 2: Token Management
1. Login to get tokens
2. Use access token for authenticated request
3. Wait for token expiry (or use expired token)
4. Refresh token using refresh token
5. Use new access token

### Scenario 3: Profile Management
1. Get current profile
2. Update profile (partial update with PATCH)
3. Update profile (full update with PUT)
4. Change password
5. Verify password change by logging in with new password

### Scenario 4: Admin Operations
1. Login as admin user
2. List all users
3. Get specific user details
4. Update user (as admin)
5. Deactivate user (soft delete)

---

## Quick Reference

### Authentication Endpoints
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/token/` - Get JWT tokens
- `POST /api/auth/token/refresh/` - Refresh access token
- `POST /api/auth/token/verify/` - Verify token

### User Management Endpoints
- `GET /api/auth/users/` - List users (Admin)
- `GET /api/auth/users/{id}/` - Get user (Admin/Owner)
- `PUT /api/auth/users/{id}/` - Update user (Admin/Owner)
- `PATCH /api/auth/users/{id}/` - Partial update (Admin/Owner)
- `DELETE /api/auth/users/{id}/` - Deactivate user (Admin)
- `GET /api/auth/users/me/` - Get current user
- `PUT /api/auth/users/me/` - Update current user
- `PATCH /api/auth/users/me/` - Partial update current user
- `POST /api/auth/users/change-password/` - Change password

---

## Tips for Testing

1. **Always save tokens** after login/register for subsequent requests
2. **Use environment variables** for base URL and tokens
3. **Test error cases** - invalid credentials, expired tokens, missing fields
4. **Check response codes** - 200/201 for success, 400 for validation errors, 401 for auth errors
5. **Use Postman Pre-request Scripts** to auto-refresh tokens if expired
6. **Test pagination** for list endpoints (if applicable)
7. **Test role-based access** - try admin endpoints as regular user

---

## Postman Collection JSON

You can import this collection directly into Postman:

```json
{
    "info": {
        "name": "Pet Health API",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "variable": [
        {
            "key": "base_url",
            "value": "http://127.0.0.1:8000"
        }
    ],
    "item": [
        {
            "name": "Authentication",
            "item": [
                {
                    "name": "Register",
                    "request": {
                        "method": "POST",
                        "header": [{"key": "Content-Type", "value": "application/json"}],
                        "body": {
                            "mode": "raw",
                            "raw": "{\n    \"email\": \"user@example.com\",\n    \"password\": \"SecurePass123!\",\n    \"password_confirm\": \"SecurePass123!\",\n    \"first_name\": \"John\",\n    \"last_name\": \"Doe\"\n}"
                        },
                        "url": {
                            "raw": "{{base_url}}/api/auth/register/",
                            "host": ["{{base_url}}"],
                            "path": ["api", "auth", "register", ""]
                        }
                    }
                },
                {
                    "name": "Login",
                    "request": {
                        "method": "POST",
                        "header": [{"key": "Content-Type", "value": "application/json"}],
                        "body": {
                            "mode": "raw",
                            "raw": "{\n    \"email\": \"user@example.com\",\n    \"password\": \"SecurePass123!\"\n}"
                        },
                        "url": {
                            "raw": "{{base_url}}/api/auth/login/",
                            "host": ["{{base_url}}"],
                            "path": ["api", "auth", "login", ""]
                        }
                    }
                }
            ]
        }
    ]
}
```

---

## Support

For issues or questions:
- Check Django server logs
- Verify database connection
- Ensure all migrations are applied
- Check environment variables in `.env` file

---

**Last Updated:** 2025-12-24

