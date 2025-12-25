# API Endpoints Documentation

Complete list of all API endpoints in Pet Health Backend.

**Base URL:** `http://127.0.0.1:8000`

**Last Updated:** 2024-01-15

---

## Authentication Endpoints

### User Registration
```
POST   /api/auth/register/
```
**Description:** Register a new user account  
**Authentication:** Not required  
**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Vishnu",
    "last_name": "Ghosh",
    "phone_number": "7292992274",
    "role": "USER"
}
```
**Response:** `201 Created` - Returns user data and JWT tokens

---

### User Login
```
POST   /api/auth/login/
```
**Description:** Authenticate user and get JWT tokens  
**Authentication:** Not required  
**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}
```
**Response:** `200 OK` - Returns user data and JWT tokens

---

### Get JWT Token
```
POST   /api/auth/token/
```
**Description:** Alternative endpoint to get JWT tokens  
**Authentication:** Not required  
**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}
```
**Response:** `200 OK` - Returns access and refresh tokens with user data

---

### Refresh JWT Token
```
POST   /api/auth/token/refresh/
```
**Description:** Refresh access token using refresh token  
**Authentication:** Not required  
**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
**Response:** `200 OK` - Returns new access token

---

### Verify JWT Token
```
POST   /api/auth/token/verify/
```
**Description:** Verify if a token is valid  
**Authentication:** Not required  
**Request Body:**
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
**Response:** `200 OK` - Empty response if valid, `401` if invalid

---

## User Management Endpoints

### Get Current User Profile
```
GET    /api/auth/users/me/
```
**Description:** Get current authenticated user's profile information  
**Authentication:** Required (Bearer Token)  
**Response:** `200 OK` - Returns user profile data

---

### Update Current User Profile
```
PUT    /api/auth/users/me/
PATCH  /api/auth/users/me/
```
**Description:** Update current user's profile (PUT for full update, PATCH for partial)  
**Authentication:** Required (Bearer Token)  
**Request Body (PATCH example):**
```json
{
    "first_name": "Vishnu",
    "last_name": "Kumar Ghosh",
    "phone_number": "9876543210",
    "is_veterinarian": true
}
```
**Response:** `200 OK` - Returns updated user data

---

### Change Password
```
POST   /api/auth/users/change-password/
```
**Description:** Change current user's password  
**Authentication:** Required (Bearer Token)  
**Request Body:**
```json
{
    "old_password": "SecurePass123!",
    "new_password": "NewPass456!",
    "new_password_confirm": "NewPass456!"
}
```
**Response:** `200 OK` - Success message

---

### List All Users
```
GET    /api/auth/users/
```
**Description:** Get list of all users (paginated)  
**Authentication:** Required (Bearer Token - Admin only)  
**Response:** `200 OK` - Returns paginated list of users

---

### Get User by ID
```
GET    /api/auth/users/{id}/
```
**Description:** Get specific user details by ID  
**Authentication:** Required (Bearer Token - Admin or Owner)  
**Response:** `200 OK` - Returns user data

---

### Update User by ID
```
PUT    /api/auth/users/{id}/
PATCH  /api/auth/users/{id}/
```
**Description:** Update user details by ID (PUT for full update, PATCH for partial)  
**Authentication:** Required (Bearer Token - Admin or Owner)  
**Request Body:**
```json
{
    "first_name": "Vishnu",
    "last_name": "Ghosh",
    "phone_number": "7061468001",
    "is_veterinarian": false
}
```
**Response:** `200 OK` - Returns updated user data

---

### Delete User (Soft Delete)
```
DELETE /api/auth/users/{id}/
```
**Description:** Deactivate user account (soft delete - sets is_active=False)  
**Authentication:** Required (Bearer Token - Admin only)  
**Response:** `200 OK` - Success message

---

## User Profile Endpoints

### Get Current User Profile
```
GET    /api/auth/profiles/me/
```
**Description:** Get current user's extended profile information  
**Authentication:** Required (Bearer Token)  
**Response:** `200 OK` - Returns profile data with phone, location, is_active

---

### Update Current User Profile
```
PUT    /api/auth/profiles/me/
PATCH  /api/auth/profiles/me/
```
**Description:** Update current user's profile (PUT for full update, PATCH for partial)  
**Authentication:** Required (Bearer Token)  
**Request Body:**
```json
{
    "phone": "9656965685",
    "location": "Noida",
    "is_active": true
}
```
**Response:** `200 OK` - Returns updated profile data

---

### Get User Profile by User ID
```
GET    /api/auth/profiles/{user_id}/
```
**Description:** Get profile of a specific user by user ID  
**Authentication:** Required (Bearer Token - Admin only)  
**Response:** `200 OK` - Returns profile data

---

### Update User Profile by User ID
```
PUT    /api/auth/profiles/{user_id}/
```
**Description:** Update profile of a specific user by user ID  
**Authentication:** Required (Bearer Token - Admin only)  
**Request Body:**
```json
{
    "phone": "7292992274",
    "location": "Noida",
    "is_active": true
}
```
**Response:** `200 OK` - Returns updated profile data

---

## Pets Endpoints

### List All Pets
```
GET    /api/pets/pets/
```
**Description:** Get list of all pets (paginated). Users see only their pets, admins see all pets  
**Authentication:** Required (Bearer Token)  
**Query Parameters:**
- `pet_type` - Filter by pet type (dog, cat, bird, rabbit, other)
- `gender` - Filter by gender (male, female, unknown)
- `search` - Search by name, breed, or microchip number
- `ordering` - Order by field (name, created_at, age, etc.)
**Response:** `200 OK` - Returns paginated list of pets

---

### Get Pet by ID
```
GET    /api/pets/pets/{id}/
```
**Description:** Get detailed information about a specific pet  
**Authentication:** Required (Bearer Token - Owner or Admin)  
**Response:** `200 OK` - Returns pet details

---

### Create Pet
```
POST   /api/pets/pets/
```
**Description:** Create a new pet. Owner is automatically set to current user  
**Authentication:** Required (Bearer Token)  
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
**Response:** `201 Created` - Returns created pet data

---

### Update Pet
```
PUT    /api/pets/pets/{id}/
PATCH  /api/pets/pets/{id}/
```
**Description:** Update pet information (PUT for full update, PATCH for partial)  
**Authentication:** Required (Bearer Token - Owner or Admin)  
**Request Body (PATCH example):**
```json
{
    "name": "Buddy Updated",
    "age": 4,
    "weight": 28.0
}
```
**Response:** `200 OK` - Returns updated pet data

---

### Delete Pet (Soft Delete)
```
DELETE /api/pets/pets/{id}/
```
**Description:** Soft delete pet (sets is_deleted=True, does not remove from database)  
**Authentication:** Required (Bearer Token - Owner or Admin)  
**Response:** `200 OK` - Success message

---

### Get My Pets
```
GET    /api/pets/pets/my_pets/
```
**Description:** Get all pets owned by current authenticated user  
**Authentication:** Required (Bearer Token)  
**Response:** `200 OK` - Returns list of user's pets

---

### Restore Pet
```
POST   /api/pets/pets/{id}/restore/
```
**Description:** Restore a soft-deleted pet  
**Authentication:** Required (Bearer Token - Owner or Admin)  
**Response:** `200 OK` - Returns restored pet data

---

## Health Endpoints

### Vaccination Endpoints

#### List All Vaccinations
```
GET    /api/health/vaccinations/
```
**Description:** List all vaccinations (filtered by user's pets for regular users, all for admins)  
**Authentication:** Required (Bearer Token)  
**Response:** `200 OK` - Returns paginated list of vaccinations

#### Get Vaccination Details
```
GET    /api/health/vaccinations/{id}/
```
**Description:** Get detailed information about a specific vaccination  
**Authentication:** Required (Bearer Token - Owner or Admin)  
**Response:** `200 OK` - Returns vaccination details

#### Create Vaccination
```
POST   /api/health/vaccinations/
```
**Description:** Create a new vaccination record for a pet  
**Authentication:** Required (Bearer Token - Owner or Admin)  
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
**Response:** `201 Created` - Returns created vaccination data

#### Update Vaccination
```
PUT    /api/health/vaccinations/{id}/
```
**Description:** Update vaccination information  
**Authentication:** Required (Bearer Token - Owner or Admin)  
**Response:** `200 OK` - Returns updated vaccination data

#### Partial Update Vaccination
```
PATCH  /api/health/vaccinations/{id}/
```
**Description:** Partially update vaccination information  
**Authentication:** Required (Bearer Token - Owner or Admin)  
**Response:** `200 OK` - Returns updated vaccination data

#### Delete Vaccination
```
DELETE /api/health/vaccinations/{id}/
```
**Description:** Delete a vaccination record  
**Authentication:** Required (Bearer Token - Owner or Admin)  
**Response:** `200 OK` - Returns success message

#### Get My Pets Vaccinations
```
GET    /api/health/vaccinations/my_pets_vaccinations/
```
**Description:** Get all vaccinations for current user's pets  
**Authentication:** Required (Bearer Token)  
**Response:** `200 OK` - Returns list of vaccinations

#### Get Pending Vaccinations
```
GET    /api/health/vaccinations/pending/
```
**Description:** Get all pending vaccinations for current user's pets  
**Authentication:** Required (Bearer Token)  
**Response:** `200 OK` - Returns list of pending vaccinations

#### Get Overdue Vaccinations
```
GET    /api/health/vaccinations/overdue/
```
**Description:** Get all overdue vaccinations for current user's pets  
**Authentication:** Required (Bearer Token)  
**Response:** `200 OK` - Returns list of overdue vaccinations

---

### Health Record Endpoints

#### List All Health Records
```
GET    /api/health/health-records/
```
**Description:** List all health records (filtered by user's pets for regular users, all for admins)  
**Authentication:** Required (Bearer Token)  
**Response:** `200 OK` - Returns paginated list of health records

#### Get Health Record Details
```
GET    /api/health/health-records/{id}/
```
**Description:** Get detailed information about a specific health record  
**Authentication:** Required (Bearer Token - Owner or Admin)  
**Response:** `200 OK` - Returns health record details

#### Create Health Record
```
POST   /api/health/health-records/
```
**Description:** Create a new health record for a pet  
**Authentication:** Required (Bearer Token - Owner or Admin)  
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
**Response:** `201 Created` - Returns created health record data

#### Update Health Record
```
PUT    /api/health/health-records/{id}/
```
**Description:** Update health record information  
**Authentication:** Required (Bearer Token - Owner or Admin)  
**Response:** `200 OK` - Returns updated health record data

#### Partial Update Health Record
```
PATCH  /api/health/health-records/{id}/
```
**Description:** Partially update health record information  
**Authentication:** Required (Bearer Token - Owner or Admin)  
**Response:** `200 OK` - Returns updated health record data

#### Delete Health Record
```
DELETE /api/health/health-records/{id}/
```
**Description:** Delete a health record  
**Authentication:** Required (Bearer Token - Owner or Admin)  
**Response:** `200 OK` - Returns success message

#### Get My Pets Health Records
```
GET    /api/health/health-records/my_pets_records/
```
**Description:** Get all health records for current user's pets  
**Authentication:** Required (Bearer Token)  
**Response:** `200 OK` - Returns list of health records

#### Get Pet Health Records
```
GET    /api/health/health-records/{id}/pet_records/
```
**Description:** Get all health records for a specific pet  
**Authentication:** Required (Bearer Token - Owner or Admin)  
**Response:** `200 OK` - Returns list of health records for the pet

---

## Appointments Endpoints

*Endpoints will be added when Appointments app is implemented*

---

## Notifications Endpoints

*Endpoints will be added when Notifications app is implemented*

---

## Subscription Endpoints

### Subscription Plan Endpoints

#### List All Subscription Plans
```
GET    /api/subscriptions/plans/
```
**Description:** List all subscription plans (active only for regular users, all for admins)  
**Authentication:** Required (Bearer Token)  
**Response:** `200 OK` - Returns paginated list of subscription plans

#### Get Subscription Plan Details
```
GET    /api/subscriptions/plans/{id}/
```
**Description:** Get detailed information about a specific subscription plan  
**Authentication:** Required (Bearer Token)  
**Response:** `200 OK` - Returns subscription plan details

#### Create Subscription Plan
```
POST   /api/subscriptions/plans/
```
**Description:** Create a new subscription plan (Admin only)  
**Authentication:** Required (Bearer Token - Admin)  
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
**Response:** `201 Created` - Returns created subscription plan data

#### Update Subscription Plan
```
PUT    /api/subscriptions/plans/{id}/
```
**Description:** Update subscription plan information (Admin only)  
**Authentication:** Required (Bearer Token - Admin)  
**Response:** `200 OK` - Returns updated subscription plan data

#### Partial Update Subscription Plan
```
PATCH  /api/subscriptions/plans/{id}/
```
**Description:** Partially update subscription plan information (Admin only)  
**Authentication:** Required (Bearer Token - Admin)  
**Response:** `200 OK` - Returns updated subscription plan data

#### Delete Subscription Plan
```
DELETE /api/subscriptions/plans/{id}/
```
**Description:** Delete a subscription plan (Admin only)  
**Authentication:** Required (Bearer Token - Admin)  
**Response:** `200 OK` - Returns success message

#### Get Active Subscription Plans
```
GET    /api/subscriptions/plans/active/
```
**Description:** Get all active subscription plans  
**Authentication:** Required (Bearer Token)  
**Response:** `200 OK` - Returns list of active subscription plans

---

### User Subscription Endpoints

#### List All User Subscriptions
```
GET    /api/subscriptions/subscriptions/
```
**Description:** List all user subscriptions (own subscriptions for users, all for admins)  
**Authentication:** Required (Bearer Token)  
**Response:** `200 OK` - Returns paginated list of user subscriptions

#### Get User Subscription Details
```
GET    /api/subscriptions/subscriptions/{id}/
```
**Description:** Get detailed information about a specific user subscription  
**Authentication:** Required (Bearer Token - Owner or Admin)  
**Response:** `200 OK` - Returns user subscription details

#### Create User Subscription
```
POST   /api/subscriptions/subscriptions/
```
**Description:** Create a new user subscription (Admin only)  
**Authentication:** Required (Bearer Token - Admin)  
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
**Response:** `201 Created` - Returns created user subscription data

#### Update User Subscription
```
PUT    /api/subscriptions/subscriptions/{id}/
```
**Description:** Update user subscription information (Admin only)  
**Authentication:** Required (Bearer Token - Admin)  
**Response:** `200 OK` - Returns updated user subscription data

#### Partial Update User Subscription
```
PATCH  /api/subscriptions/subscriptions/{id}/
```
**Description:** Partially update user subscription information (Admin only)  
**Authentication:** Required (Bearer Token - Admin)  
**Response:** `200 OK` - Returns updated user subscription data

#### Delete User Subscription
```
DELETE /api/subscriptions/subscriptions/{id}/
```
**Description:** Delete a user subscription (Admin only)  
**Authentication:** Required (Bearer Token - Admin)  
**Response:** `200 OK` - Returns success message

#### Get My Active Subscription
```
GET    /api/subscriptions/subscriptions/my_subscription/
```
**Description:** Get current user's active subscription  
**Authentication:** Required (Bearer Token)  
**Response:** `200 OK` - Returns active subscription data or 404 if not found

#### Get My Current Subscription
```
GET    /api/subscriptions/subscriptions/current/
```
**Description:** Get current user's subscription (active or most recent)  
**Authentication:** Required (Bearer Token)  
**Response:** `200 OK` - Returns subscription data or 404 if not found

#### Get My All Subscriptions
```
GET    /api/subscriptions/subscriptions/my_subscriptions/
```
**Description:** Get all subscriptions for current user  
**Authentication:** Required (Bearer Token)  
**Response:** `200 OK` - Returns list of user subscriptions

#### Cancel Subscription
```
POST   /api/subscriptions/subscriptions/{id}/cancel/
```
**Description:** Cancel a user subscription (Admin only)  
**Authentication:** Required (Bearer Token - Admin)  
**Response:** `200 OK` - Returns cancelled subscription data

---

## Admin Panel

### Django Admin Interface
```
GET    /admin/
```
**Description:** Django admin panel for internal management  
**Authentication:** Required (Admin credentials)  
**Access:** Admin users only

---

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

###  Important Notes:

1. **GET Requests:** Body meain data nahi bhejte hai  Authentication Header mein  hota hai
2. **POST/PUT/PATCH:** Body meain data bhejte hai + Header meain token
3. **Token Format:** `Bearer <space><token>` (space mandatory hai )

### Postman Setup:

**Authorization Tab:**
- Type: `Bearer Token`
- Token: Paste your access token here

**OR Headers Tab:**
- Key: `Authorization`
- Value: `Bearer <your_access_token>`

## Response Formats

### Success Response
```json
{
    "message": "Operation successful",
    "data": { ... }
}
```

### Error Response
```json
{
    "detail": "Error message",
    "field_name": ["Field-specific error"]
}
```

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

**Note:** This file should be updated whenever new API endpoints are added to the project.

