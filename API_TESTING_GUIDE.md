# API Testing Guide - Postman

Complete guide for testing all Pet Health Backend APIs using Postman.

## Table of Contents
1. [Setup](#setup)
2. [Authentication Flow](#authentication-flow)
3. [User Management APIs](#user-management-apis)
4. [User Profile Endpoints](#user-profile-endpoints)
5. [Pet Management APIs](#pet-management-apis)
6. [Health Management APIs](#health-management-apis)
7. [Subscription Management APIs](#subscription-management-apis)
8. [Postman Collection Setup](#postman-collection-setup)
9. [Testing Examples](#testing-examples)
10. [Error Responses](#error-responses)
11. [Common Testing Scenarios](#common-testing-scenarios)
12. [Quick Reference](#quick-reference)

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
    "last_name": "Mishra",
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
        "first_name": "Satyam",
        "last_name": "Mishra",
        "full_name": "Satyam Mishra",
        "phone_number": "7292992274",
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
        "first_name": "Satyam",
        "last_name": "Mishra",
        "full_name": "Satyam Mishra",
        "phone_number": "729292274",
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
        "first_name": "Satyam",
        "last_name": "Mishra",
        "full_name": "Satyam Mishra",
        "phone_number": "7292992274",
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
    "first_name": "Satyam",
    "last_name": "Mishra",
    "full_name": "Satyam Mishra",
    "phone_number": "7292992274",
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
    "first_name": "Satyam",
    "last_name": "Mishra",
    "phone_number": "9876543210",
    "is_veterinarian": true
}
```

**Request Body (PATCH - Partial Update):**
```json
{
    "first_name": "Satyam Kumar"
}
```

**Response (200 OK):**
```json
{
    "message": "Profile updated successfully.",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "Satyam Kumar",
        "last_name": "Mishra",
        "full_name": "Satyam Kumar Mishra",
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
    "first_name": "Satyam Kumar",
    "last_name": "Mishra",
    "full_name": "Satyam Kumar Mishra",
    "phone_number": "+9876543210",
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
    "first_name": "Vishn",
    "last_name": "Ghosh",
    "phone_number": "+9876543210",
    "is_veterinarian": false
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "email": "user@example.com",
    "first_name": "Vishnu",
    "last_name": "Ghosh",
    "full_name": "Vishnu Ghosh",
    "phone_number": "+9876543210",
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

## User Profile Endpoints

### 13. Get Current User Profile

**Endpoint:** `GET /api/auth/profiles/me/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Profile retrieved successfully.",
    "data": {
        "id": 1,
        "user": 1,
        "user_email": "user@example.com",
        "user_full_name": "Satyam Mishra",
        "phone": "7292992274",
        "location": "Noida",
        "is_active": true,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
}
```

---

### 14. Update Current User Profile

**Endpoint:** `PUT /api/auth/profiles/me/` or `PATCH /api/auth/profiles/me/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body (PATCH example):**
```json
{
    "phone": "9876543210",
    "location": "Delhi",
    "is_active": true
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Profile updated successfully.",
    "data": {
        "id": 1,
        "user": 1,
        "user_email": "user@example.com",
        "user_full_name": "Satyam Mishra",
        "phone": "9876543210",
        "location": "Delhi",
        "is_active": true,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T11:00:00Z"
    }
}
```

---

### 15. Get User Profile by User ID (Admin Only)

**Endpoint:** `GET /api/auth/profiles/{user_id}/`

**Headers:**
```
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Profile retrieved successfully.",
    "data": {
        "id": 1,
        "user": 1,
        "user_email": "user@example.com",
        "user_full_name": "Satyam Mishra",
        "phone": "7292992274",
        "location": "Noida",
        "is_active": true,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
}
```

---

### 16. Update User Profile by User ID (Admin Only)

**Endpoint:** `PUT /api/auth/profiles/{user_id}/`

**Headers:**
```
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "phone": "7292992274",
    "location": "Noida",
    "is_active": true
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Profile updated successfully.",
    "data": {
        "id": 1,
        "user": 1,
        "user_email": "user@example.com",
        "user_full_name": "Satyam Mishra",
        "phone": "7292992274",
        "location": "Noida",
        "is_active": true,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T11:00:00Z"
    }
}
```

---

## Pet Management APIs

### 17. List All Pets

**Endpoint:** `GET /api/pets/pets/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Query Parameters:**
- `pet_type` - Filter by pet type (dog, cat, bird, rabbit, other)
- `gender` - Filter by gender (male, female, unknown)
- `search` - Search by name, breed, or microchip number
- `ordering` - Order by field (name, created_at, age, etc.)

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Pets retrieved successfully.",
    "data": {
        "count": 5,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "Buddy",
                "breed": "Golden Retriever",
                "age": 3,
                "weight": 25.5,
                "gender": "male",
                "pet_type": "dog",
                "owner": 1,
                "owner_name": "Satyam Mishra",
                "created_at": "2024-01-15T10:30:00Z"
            }
        ]
    }
}
```

---

### 18. Get Pet by ID

**Endpoint:** `GET /api/pets/pets/{id}/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Pet retrieved successfully.",
    "data": {
        "id": 1,
        "name": "Buddy",
        "breed": "Golden Retriever",
        "age": 3,
        "weight": 25.5,
        "gender": "male",
        "pet_type": "dog",
        "date_of_birth": "2021-01-15",
        "color": "Golden",
        "microchip_number": "ABC123456",
        "notes": "Friendly and active",
        "owner": 1,
        "owner_name": "Satyam Mishra",
        "owner_email": "user@example.com",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
}
```

---

### 19. Create Pet

**Endpoint:** `POST /api/pets/pets/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "name": "Buddy",
    "breed": "Golden Retriever",
    "age": 3,
    "weight": 25.5,
    "gender": "male",
    "pet_type": "dog",
    "date_of_birth": "2021-01-15",
    "color": "Golden",
    "microchip_number": "ABC123456",
    "notes": "Friendly and active"
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "Pet created successfully.",
    "data": {
        "id": 1,
        "name": "Buddy",
        "breed": "Golden Retriever",
        "age": 3,
        "weight": 25.5,
        "gender": "male",
        "pet_type": "dog",
        "date_of_birth": "2021-01-15",
        "color": "Golden",
        "microchip_number": "ABC123456",
        "notes": "Friendly and active",
        "owner": 1,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
}
```

---

### 20. Update Pet

**Endpoint:** `PUT /api/pets/pets/{id}/` or `PATCH /api/pets/pets/{id}/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body (PATCH example):**
```json
{
    "name": "Buddy Updated",
    "age": 4,
    "weight": 28.0
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Pet updated successfully.",
    "data": {
        "id": 1,
        "name": "Buddy Updated",
        "breed": "Golden Retriever",
        "age": 4,
        "weight": 28.0,
        "gender": "male",
        "pet_type": "dog",
        "owner": 1,
        "updated_at": "2024-01-15T11:00:00Z"
    }
}
```

---

### 21. Delete Pet (Soft Delete)

**Endpoint:** `DELETE /api/pets/pets/{id}/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Pet deleted successfully."
}
```

**Note:** This performs a soft delete (sets `is_deleted=True`), the pet is not removed from the database.

---

### 22. Get My Pets

**Endpoint:** `GET /api/pets/pets/my_pets/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Pets retrieved successfully.",
    "data": [
        {
            "id": 1,
            "name": "Buddy",
            "breed": "Golden Retriever",
            "age": 3,
            "weight": 25.5,
            "gender": "male",
            "pet_type": "dog",
            "owner": 1,
            "created_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

---

### 23. Restore Pet

**Endpoint:** `POST /api/pets/pets/{id}/restore/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Pet restored successfully.",
    "data": {
        "id": 1,
        "name": "Buddy",
        "breed": "Golden Retriever",
        "is_deleted": false,
        "deleted_at": null
    }
}
```

---

## Health Management APIs

### Vaccination Endpoints

### 24. List All Vaccinations

**Endpoint:** `GET /api/health/vaccinations/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Vaccinations retrieved successfully.",
    "data": {
        "count": 10,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "pet": 1,
                "pet_name": "Buddy",
                "vaccine_name": "Rabies",
                "due_date": "2025-01-15",
                "status": "pending",
                "administered_date": null,
                "veterinarian": null,
                "batch_number": "BATCH123",
                "notes": "Annual vaccination",
                "created_at": "2024-01-15T10:30:00Z"
            }
        ]
    }
}
```

---

### 25. Get Vaccination Details

**Endpoint:** `GET /api/health/vaccinations/{id}/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Vaccination retrieved successfully.",
    "data": {
        "id": 1,
        "pet": 1,
        "pet_name": "Buddy",
        "pet_breed": "Golden Retriever",
        "pet_owner": "Satyam Mishra",
        "vaccine_name": "Rabies",
        "due_date": "2025-01-15",
        "status": "pending",
        "administered_date": null,
        "veterinarian": null,
        "veterinarian_name": null,
        "batch_number": "BATCH123",
        "notes": "Annual vaccination",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
}
```

---

### 26. Create Vaccination

**Endpoint:** `POST /api/health/vaccinations/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "pet": 1,
    "vaccine_name": "Rabies",
    "due_date": "2025-01-15",
    "status": "pending",
    "administered_date": null,
    "veterinarian": null,
    "batch_number": "BATCH123",
    "notes": "Annual vaccination"
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "Vaccination created successfully.",
    "data": {
        "id": 1,
        "pet": 1,
        "vaccine_name": "Rabies",
        "due_date": "2025-01-15",
        "status": "pending",
        "administered_date": null,
        "veterinarian": null,
        "batch_number": "BATCH123",
        "notes": "Annual vaccination",
        "created_at": "2024-01-15T10:30:00Z"
    }
}
```

---

### 27. Update Vaccination

**Endpoint:** `PUT /api/health/vaccinations/{id}/` or `PATCH /api/health/vaccinations/{id}/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body (PATCH example):**
```json
{
    "status": "completed",
    "administered_date": "2025-01-10",
    "notes": "Vaccination completed successfully"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Vaccination updated successfully.",
    "data": {
        "id": 1,
        "status": "completed",
        "administered_date": "2025-01-10",
        "notes": "Vaccination completed successfully",
        "updated_at": "2024-01-15T11:00:00Z"
    }
}
```

---

### 28. Delete Vaccination

**Endpoint:** `DELETE /api/health/vaccinations/{id}/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Vaccination deleted successfully."
}
```

---

### 29. Get My Pets Vaccinations

**Endpoint:** `GET /api/health/vaccinations/my_pets_vaccinations/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Vaccinations retrieved successfully.",
    "data": [
        {
            "id": 1,
            "pet": 1,
            "pet_name": "Buddy",
            "vaccine_name": "Rabies",
            "due_date": "2025-01-15",
            "status": "pending"
        }
    ]
}
```

---

### 30. Get Pending Vaccinations

**Endpoint:** `GET /api/health/vaccinations/pending/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Pending vaccinations retrieved successfully.",
    "data": [
        {
            "id": 1,
            "pet": 1,
            "pet_name": "Buddy",
            "vaccine_name": "Rabies",
            "due_date": "2025-01-15",
            "status": "pending"
        }
    ]
}
```

---

### 31. Get Overdue Vaccinations

**Endpoint:** `GET /api/health/vaccinations/overdue/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Overdue vaccinations retrieved successfully.",
    "data": [
        {
            "id": 1,
            "pet": 1,
            "pet_name": "Buddy",
            "vaccine_name": "Rabies",
            "due_date": "2024-12-15",
            "status": "pending"
        }
    ]
}
```

---

### Health Record Endpoints

### 32. List All Health Records

**Endpoint:** `GET /api/health/health-records/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Health records retrieved successfully.",
    "data": {
        "count": 5,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "pet": 1,
                "pet_name": "Buddy",
                "weight": 25.5,
                "record_date": "2025-01-10",
                "temperature": 38.5,
                "heart_rate": 120,
                "veterinarian": null,
                "created_at": "2024-01-15T10:30:00Z"
            }
        ]
    }
}
```

---

### 33. Get Health Record Details

**Endpoint:** `GET /api/health/health-records/{id}/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Health record retrieved successfully.",
    "data": {
        "id": 1,
        "pet": 1,
        "pet_name": "Buddy",
        "pet_breed": "Golden Retriever",
        "pet_owner": "Satyam Mishra",
        "weight": 25.5,
        "notes": "Regular checkup, all good",
        "record_date": "2025-01-10",
        "veterinarian": null,
        "veterinarian_name": null,
        "temperature": 38.5,
        "heart_rate": 120,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
}
```

---

### 34. Create Health Record

**Endpoint:** `POST /api/health/health-records/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "pet": 1,
    "weight": 25.5,
    "notes": "Regular checkup, all good",
    "record_date": "2025-01-10",
    "veterinarian": null,
    "temperature": 38.5,
    "heart_rate": 120
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "Health record created successfully.",
    "data": {
        "id": 1,
        "pet": 1,
        "weight": 25.5,
        "notes": "Regular checkup, all good",
        "record_date": "2025-01-10",
        "veterinarian": null,
        "temperature": 38.5,
        "heart_rate": 120,
        "created_at": "2024-01-15T10:30:00Z"
    }
}
```

---

### 35. Update Health Record

**Endpoint:** `PUT /api/health/health-records/{id}/` or `PATCH /api/health/health-records/{id}/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body (PATCH example):**
```json
{
    "weight": 26.0,
    "notes": "Weight increased, healthy"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Health record updated successfully.",
    "data": {
        "id": 1,
        "weight": 26.0,
        "notes": "Weight increased, healthy",
        "updated_at": "2024-01-15T11:00:00Z"
    }
}
```

---

### 36. Delete Health Record

**Endpoint:** `DELETE /api/health/health-records/{id}/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Health record deleted successfully."
}
```

---

### 37. Get My Pets Health Records

**Endpoint:** `GET /api/health/health-records/my_pets_records/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Health records retrieved successfully.",
    "data": [
        {
            "id": 1,
            "pet": 1,
            "pet_name": "Buddy",
            "weight": 25.5,
            "record_date": "2025-01-10",
            "temperature": 38.5,
            "heart_rate": 120
        }
    ]
}
```

---

### 38. Get Pet Health Records

**Endpoint:** `GET /api/health/health-records/{id}/pet_records/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Health records retrieved successfully.",
    "data": [
        {
            "id": 1,
            "pet": 1,
            "weight": 25.5,
            "record_date": "2025-01-10",
            "temperature": 38.5,
            "heart_rate": 120
        }
    ]
}
```

---

## Subscription Management APIs

### Subscription Plan Endpoints

### 39. List All Subscription Plans

**Endpoint:** `GET /api/subscriptions/plans/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Subscription plans retrieved successfully.",
    "data": {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "plan_type": "free",
                "name": "Free Plan",
                "description": "Basic features",
                "price": 0.00,
                "duration_days": 30,
                "is_active": true,
                "features": ["Basic features"],
                "max_pets": 2
            },
            {
                "id": 2,
                "plan_type": "premium",
                "name": "Premium Plan",
                "description": "Premium features",
                "price": 29.99,
                "duration_days": 30,
                "is_active": true,
                "features": ["Unlimited pets", "Priority support"],
                "max_pets": 10
            }
        ]
    }
}
```

---

### 40. Get Subscription Plan Details

**Endpoint:** `GET /api/subscriptions/plans/{id}/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Subscription plan retrieved successfully.",
    "data": {
        "id": 1,
        "plan_type": "premium",
        "name": "Premium Plan",
        "description": "Premium subscription with advanced features",
        "price": 29.99,
        "duration_days": 30,
        "is_active": true,
        "features": ["Unlimited pets", "Priority support", "Advanced analytics"],
        "max_pets": 10,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
}
```

---

### 41. Create Subscription Plan (Admin Only)

**Endpoint:** `POST /api/subscriptions/plans/`

**Headers:**
```
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "plan_type": "premium",
    "name": "Premium Plan",
    "description": "Premium subscription with advanced features",
    "price": 29.99,
    "duration_days": 30,
    "is_active": true,
    "features": ["Unlimited pets", "Priority support", "Advanced analytics"],
    "max_pets": 10
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "Subscription plan created successfully.",
    "data": {
        "id": 1,
        "plan_type": "premium",
        "name": "Premium Plan",
        "description": "Premium subscription with advanced features",
        "price": 29.99,
        "duration_days": 30,
        "is_active": true,
        "features": ["Unlimited pets", "Priority support", "Advanced analytics"],
        "max_pets": 10,
        "created_at": "2024-01-15T10:30:00Z"
    }
}
```

---

### 42. Update Subscription Plan (Admin Only)

**Endpoint:** `PUT /api/subscriptions/plans/{id}/` or `PATCH /api/subscriptions/plans/{id}/`

**Headers:**
```
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

**Request Body (PATCH example):**
```json
{
    "price": 39.99,
    "features": ["Unlimited pets", "Priority support", "Advanced analytics", "24/7 Support"]
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Subscription plan updated successfully.",
    "data": {
        "id": 1,
        "price": 39.99,
        "features": ["Unlimited pets", "Priority support", "Advanced analytics", "24/7 Support"],
        "updated_at": "2024-01-15T11:00:00Z"
    }
}
```

---

### 43. Delete Subscription Plan (Admin Only)

**Endpoint:** `DELETE /api/subscriptions/plans/{id}/`

**Headers:**
```
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Subscription plan deleted successfully."
}
```

---

### 44. Get Active Subscription Plans

**Endpoint:** `GET /api/subscriptions/plans/active/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Active subscription plans retrieved successfully.",
    "data": [
        {
            "id": 1,
            "plan_type": "free",
            "name": "Free Plan",
            "price": 0.00,
            "is_active": true
        },
        {
            "id": 2,
            "plan_type": "premium",
            "name": "Premium Plan",
            "price": 29.99,
            "is_active": true
        }
    ]
}
```

---

### User Subscription Endpoints

### 45. List All User Subscriptions

**Endpoint:** `GET /api/subscriptions/subscriptions/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "User subscriptions retrieved successfully.",
    "data": {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "user": 1,
                "user_email": "user@example.com",
                "plan": 1,
                "plan_name": "Premium Plan",
                "start_date": "2025-01-01",
                "end_date": "2025-01-31",
                "status": "active",
                "is_active": true,
                "auto_renew": false
            }
        ]
    }
}
```

---

### 46. Get User Subscription Details

**Endpoint:** `GET /api/subscriptions/subscriptions/{id}/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "User subscription retrieved successfully.",
    "data": {
        "id": 1,
        "user": 1,
        "user_email": "user@example.com",
        "user_full_name": "Satyam Mishra",
        "plan": 1,
        "plan_name": "Premium Plan",
        "plan_type": "premium",
        "start_date": "2025-01-01",
        "end_date": "2025-01-31",
        "status": "active",
        "is_active": true,
        "auto_renew": false,
        "cancelled_at": null,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
}
```

---

### 47. Create User Subscription (Admin Only)

**Endpoint:** `POST /api/subscriptions/subscriptions/`

**Headers:**
```
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "user": 1,
    "plan": 1,
    "start_date": "2025-01-01",
    "end_date": "2025-01-31",
    "status": "active",
    "auto_renew": false
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "User subscription created successfully.",
    "data": {
        "id": 1,
        "user": 1,
        "plan": 1,
        "start_date": "2025-01-01",
        "end_date": "2025-01-31",
        "status": "active",
        "is_active": true,
        "auto_renew": false,
        "created_at": "2024-01-15T10:30:00Z"
    }
}
```

---

### 48. Update User Subscription (Admin Only)

**Endpoint:** `PUT /api/subscriptions/subscriptions/{id}/` or `PATCH /api/subscriptions/subscriptions/{id}/`

**Headers:**
```
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

**Request Body (PATCH example):**
```json
{
    "status": "cancelled",
    "auto_renew": false
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "User subscription updated successfully.",
    "data": {
        "id": 1,
        "status": "cancelled",
        "is_active": false,
        "auto_renew": false,
        "cancelled_at": "2024-01-15T11:00:00Z",
        "updated_at": "2024-01-15T11:00:00Z"
    }
}
```

---

### 49. Delete User Subscription (Admin Only)

**Endpoint:** `DELETE /api/subscriptions/subscriptions/{id}/`

**Headers:**
```
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "User subscription deleted successfully."
}
```

---

### 50. Get My Active Subscription

**Endpoint:** `GET /api/subscriptions/subscriptions/my_subscription/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Active subscription retrieved successfully.",
    "data": {
        "id": 1,
        "user": 1,
        "plan": 1,
        "plan_name": "Premium Plan",
        "start_date": "2025-01-01",
        "end_date": "2025-01-31",
        "status": "active",
        "is_active": true
    }
}
```

**Response (404 Not Found) - No Active Subscription:**
```json
{
    "success": false,
    "message": "No active subscription found.",
    "errors": {}
}
```

---

### 51. Get My Current Subscription

**Endpoint:** `GET /api/subscriptions/subscriptions/current/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Current subscription retrieved successfully.",
    "data": {
        "id": 1,
        "user": 1,
        "plan": 1,
        "plan_name": "Premium Plan",
        "start_date": "2025-01-01",
        "end_date": "2025-01-31",
        "status": "active",
        "is_active": true
    }
}
```

---

### 52. Get My All Subscriptions

**Endpoint:** `GET /api/subscriptions/subscriptions/my_subscriptions/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "User subscriptions retrieved successfully.",
    "data": [
        {
            "id": 1,
            "plan": 1,
            "plan_name": "Premium Plan",
            "start_date": "2025-01-01",
            "end_date": "2025-01-31",
            "status": "active",
            "is_active": true
        }
    ]
}
```

---

### 53. Cancel Subscription (Admin Only)

**Endpoint:** `POST /api/subscriptions/subscriptions/{id}/cancel/`

**Headers:**
```
Authorization: Bearer <admin_access_token>
Content-Type: application/json
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Subscription cancelled successfully.",
    "data": {
        "id": 1,
        "status": "cancelled",
        "is_active": false,
        "cancelled_at": "2024-01-15T11:00:00Z"
    }
}
```

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

### Scenario 5: Pet Management Flow
1. Create a new pet
2. List all my pets
3. Get pet details
4. Update pet information
5. Create vaccination record for pet
6. Create health record for pet
7. Soft delete pet
8. Restore pet

### Scenario 6: Health Management Flow
1. Create vaccination record
2. List all vaccinations
3. Get pending vaccinations
4. Get overdue vaccinations
5. Update vaccination status
6. Create health record
7. List health records for a pet
8. Update health record

### Scenario 7: Subscription Management Flow
1. List all subscription plans
2. Get active plans
3. Create user subscription (Admin)
4. Get my active subscription
5. Get my all subscriptions
6. Cancel subscription (Admin)

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

### User Profile Endpoints
- `GET /api/auth/profiles/me/` - Get current user profile
- `PUT /api/auth/profiles/me/` - Update current user profile
- `PATCH /api/auth/profiles/me/` - Partial update current user profile
- `GET /api/auth/profiles/{user_id}/` - Get user profile by ID (Admin)
- `PUT /api/auth/profiles/{user_id}/` - Update user profile by ID (Admin)

### Pet Management Endpoints
- `GET /api/pets/pets/` - List all pets
- `GET /api/pets/pets/{id}/` - Get pet by ID
- `POST /api/pets/pets/` - Create pet
- `PUT /api/pets/pets/{id}/` - Update pet
- `PATCH /api/pets/pets/{id}/` - Partial update pet
- `DELETE /api/pets/pets/{id}/` - Soft delete pet
- `GET /api/pets/pets/my_pets/` - Get my pets
- `POST /api/pets/pets/{id}/restore/` - Restore soft-deleted pet

### Health Management Endpoints

#### Vaccination Endpoints
- `GET /api/health/vaccinations/` - List all vaccinations
- `GET /api/health/vaccinations/{id}/` - Get vaccination details
- `POST /api/health/vaccinations/` - Create vaccination
- `PUT /api/health/vaccinations/{id}/` - Update vaccination
- `PATCH /api/health/vaccinations/{id}/` - Partial update vaccination
- `DELETE /api/health/vaccinations/{id}/` - Delete vaccination
- `GET /api/health/vaccinations/my_pets_vaccinations/` - Get my pets vaccinations
- `GET /api/health/vaccinations/pending/` - Get pending vaccinations
- `GET /api/health/vaccinations/overdue/` - Get overdue vaccinations

#### Health Record Endpoints
- `GET /api/health/health-records/` - List all health records
- `GET /api/health/health-records/{id}/` - Get health record details
- `POST /api/health/health-records/` - Create health record
- `PUT /api/health/health-records/{id}/` - Update health record
- `PATCH /api/health/health-records/{id}/` - Partial update health record
- `DELETE /api/health/health-records/{id}/` - Delete health record
- `GET /api/health/health-records/my_pets_records/` - Get my pets health records
- `GET /api/health/health-records/{id}/pet_records/` - Get pet health records

### Subscription Management Endpoints

#### Subscription Plan Endpoints
- `GET /api/subscriptions/plans/` - List all subscription plans
- `GET /api/subscriptions/plans/{id}/` - Get subscription plan details
- `POST /api/subscriptions/plans/` - Create subscription plan (Admin)
- `PUT /api/subscriptions/plans/{id}/` - Update subscription plan (Admin)
- `PATCH /api/subscriptions/plans/{id}/` - Partial update subscription plan (Admin)
- `DELETE /api/subscriptions/plans/{id}/` - Delete subscription plan (Admin)
- `GET /api/subscriptions/plans/active/` - Get active subscription plans

#### User Subscription Endpoints
- `GET /api/subscriptions/subscriptions/` - List all user subscriptions
- `GET /api/subscriptions/subscriptions/{id}/` - Get user subscription details
- `POST /api/subscriptions/subscriptions/` - Create user subscription (Admin)
- `PUT /api/subscriptions/subscriptions/{id}/` - Update user subscription (Admin)
- `PATCH /api/subscriptions/subscriptions/{id}/` - Partial update user subscription (Admin)
- `DELETE /api/subscriptions/subscriptions/{id}/` - Delete user subscription (Admin)
- `GET /api/subscriptions/subscriptions/my_subscription/` - Get my active subscription
- `GET /api/subscriptions/subscriptions/current/` - Get my current subscription
- `GET /api/subscriptions/subscriptions/my_subscriptions/` - Get my all subscriptions
- `POST /api/subscriptions/subscriptions/{id}/cancel/` - Cancel subscription (Admin)

---

## Tips for Testing

1. **Always save tokens** after login/register for subsequent requests
2. **Use environment variables** for base URL and tokens
3. **Test error cases** - invalid credentials, expired tokens, missing fields
4. **Check response codes** - 200/201 for success, 400 for validation errors, 401 for auth errors
5. **Use Postman Pre-request Scripts** to auto-refresh tokens if expired
6. **Test pagination** for list endpoints (if applicable)
7. **Test role-based access** - try admin endpoints as regular user
8. **Test ownership** - try accessing other users' pets, health records, subscriptions
9. **Test soft delete** - verify pets can be restored after deletion
10. **Test date validations** - try past dates for appointments, future dates for vaccinations
11. **Test query parameters** - use filters, search, and ordering for list endpoints
12. **Test partial updates** - use PATCH for updating only specific fields

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

**Last Updated:** 2025-12-25

