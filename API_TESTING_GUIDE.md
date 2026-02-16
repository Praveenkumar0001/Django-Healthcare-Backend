# API Testing Guide

This guide provides example requests and responses for testing all API endpoints.

## Setup

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. Base URL: `http://127.0.0.1:8000/api/`

## 1. Authentication Flow

### Step 1: Register a New User

**Request:**
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "healthcare_admin",
    "email": "admin@healthcare.com",
    "first_name": "Healthcare",
    "last_name": "Admin",
    "password": "SecurePass123!@",
    "password2": "SecurePass123!@"
}
```

**Expected Response (201 Created):**
```json
{
    "success": true,
    "message": "User registered successfully",
    "data": {
        "user": {
            "id": 1,
            "username": "healthcare_admin",
            "email": "admin@healthcare.com",
            "first_name": "Healthcare",
            "last_name": "Admin"
        }
    }
}
```

### Step 2: Login

**Request:**
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "healthcare_admin",
    "password": "SecurePass123!@"
}
```

**Expected Response (200 OK):**
```json
{
    "success": true,
    "message": "Login successful",
    "data": {
        "user": {
            "id": 1,
            "username": "healthcare_admin",
            "email": "admin@healthcare.com",
            "first_name": "Healthcare",
            "last_name": "Admin"
        },
        "tokens": {
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
        }
    }
}
```

**Important:** Save the `access` token for subsequent requests!

## 2. Patient Management

### Create a Patient

**Request:**
```http
POST /api/patients/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
    "name": "Alice Johnson",
    "email": "alice.johnson@email.com",
    "phone": "+11234567890",
    "date_of_birth": "1985-03-20",
    "gender": "F",
    "address": "456 Oak Avenue, Springfield, IL 62701",
    "medical_history": "Allergic to penicillin. History of asthma."
}
```

**Expected Response (201 Created):**
```json
{
    "success": true,
    "message": "Patient created successfully",
    "data": {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@email.com",
        "phone": "+11234567890",
        "date_of_birth": "1985-03-20",
        "gender": "F",
        "address": "456 Oak Avenue, Springfield, IL 62701",
        "medical_history": "Allergic to penicillin. History of asthma.",
        "created_by": {
            "id": 1,
            "username": "healthcare_admin",
            "email": "admin@healthcare.com",
            "first_name": "Healthcare",
            "last_name": "Admin"
        },
        "created_at": "2026-02-16T10:30:00Z",
        "updated_at": "2026-02-16T10:30:00Z"
    }
}
```

### Get All Patients

**Request:**
```http
GET /api/patients/
Authorization: Bearer <your_access_token>
```

**Expected Response (200 OK):**
```json
{
    "success": true,
    "message": "Patients retrieved successfully",
    "data": [
        {
            "id": 1,
            "name": "Alice Johnson",
            "email": "alice.johnson@email.com",
            ...
        }
    ]
}
```

### Get Specific Patient

**Request:**
```http
GET /api/patients/1/
Authorization: Bearer <your_access_token>
```

### Update Patient

**Request (Partial Update - PATCH):**
```http
PATCH /api/patients/1/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
    "phone": "+11234567899",
    "address": "789 New Street, Springfield, IL 62701"
}
```

**Request (Full Update - PUT):**
```http
PUT /api/patients/1/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
    "name": "Alice Johnson",
    "email": "alice.johnson@email.com",
    "phone": "+11234567899",
    "date_of_birth": "1985-03-20",
    "gender": "F",
    "address": "789 New Street, Springfield, IL 62701",
    "medical_history": "Allergic to penicillin. History of asthma. Updated."
}
```

### Delete Patient

**Request:**
```http
DELETE /api/patients/1/
Authorization: Bearer <your_access_token>
```

**Expected Response (200 OK):**
```json
{
    "success": true,
    "message": "Patient deleted successfully",
    "data": null
}
```

## 3. Doctor Management

### Create a Doctor

**Request:**
```http
POST /api/doctors/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
    "name": "Dr. Robert Smith",
    "email": "dr.smith@hospital.com",
    "phone": "+19876543210",
    "specialization": "CARDIOLOGY",
    "license_number": "MD-CARD-2024-001",
    "years_of_experience": 15
}
```

**Expected Response (201 Created):**
```json
{
    "success": true,
    "message": "Doctor created successfully",
    "data": {
        "id": 1,
        "name": "Dr. Robert Smith",
        "email": "dr.smith@hospital.com",
        "phone": "+19876543210",
        "specialization": "CARDIOLOGY",
        "license_number": "MD-CARD-2024-001",
        "years_of_experience": 15,
        "created_by": {
            "id": 1,
            "username": "healthcare_admin",
            "email": "admin@healthcare.com",
            "first_name": "Healthcare",
            "last_name": "Admin"
        },
        "created_at": "2026-02-16T10:35:00Z",
        "updated_at": "2026-02-16T10:35:00Z"
    }
}
```

### Get All Doctors

**Request:**
```http
GET /api/doctors/
Authorization: Bearer <your_access_token>
```

### Get Specific Doctor

**Request:**
```http
GET /api/doctors/1/
Authorization: Bearer <your_access_token>
```

### Update Doctor

**Request:**
```http
PATCH /api/doctors/1/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
    "years_of_experience": 16
}
```

### Delete Doctor

**Request:**
```http
DELETE /api/doctors/1/
Authorization: Bearer <your_access_token>
```

## 4. Patient-Doctor Mapping

### Assign Doctor to Patient

**Request:**
```http
POST /api/mappings/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
    "patient": 1,
    "doctor": 1,
    "notes": "Regular cardiology checkup scheduled for next month"
}
```

**Expected Response (201 Created):**
```json
{
    "success": true,
    "message": "Doctor assigned to patient successfully",
    "data": {
        "id": 1,
        "patient": 1,
        "doctor": 1,
        "patient_details": {
            "id": 1,
            "name": "Alice Johnson",
            "email": "alice.johnson@email.com",
            ...
        },
        "doctor_details": {
            "id": 1,
            "name": "Dr. Robert Smith",
            "email": "dr.smith@hospital.com",
            ...
        },
        "assigned_date": "2026-02-16T10:40:00Z",
        "notes": "Regular cardiology checkup scheduled for next month",
        "created_by": {
            "id": 1,
            "username": "healthcare_admin",
            ...
        }
    }
}
```

### Get All Mappings

**Request:**
```http
GET /api/mappings/
Authorization: Bearer <your_access_token>
```

**Expected Response (200 OK):**
```json
{
    "success": true,
    "message": "All patient-doctor mappings retrieved successfully",
    "data": [
        {
            "id": 1,
            "patient": 1,
            "patient_name": "Alice Johnson",
            "doctor": 1,
            "doctor_name": "Dr. Robert Smith",
            "assigned_date": "2026-02-16T10:40:00Z",
            "notes": "Regular cardiology checkup scheduled for next month"
        }
    ]
}
```

### Get Doctors for Specific Patient

**Request:**
```http
GET /api/mappings/?patient_id=1
Authorization: Bearer <your_access_token>
```

**Expected Response (200 OK):**
```json
{
    "success": true,
    "message": "Doctors assigned to patient retrieved successfully",
    "data": [
        {
            "id": 1,
            "patient": 1,
            "patient_name": "Alice Johnson",
            "doctor": 1,
            "doctor_name": "Dr. Robert Smith",
            "assigned_date": "2026-02-16T10:40:00Z",
            "notes": "Regular cardiology checkup scheduled for next month"
        }
    ]
}
```

### Remove Doctor from Patient

**Request:**
```http
DELETE /api/mappings/1/
Authorization: Bearer <your_access_token>
```

**Expected Response (200 OK):**
```json
{
    "success": true,
    "message": "Doctor removed from patient successfully",
    "data": null
}
```

## 5. Error Scenarios

### Missing Required Fields

**Request:**
```http
POST /api/patients/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
    "name": "John Doe"
}
```

**Expected Response (400 Bad Request):**
```json
{
    "success": false,
    "error": {
        "message": "Failed to create patient",
        "details": {
            "email": ["This field is required."],
            "phone": ["This field is required."],
            "date_of_birth": ["This field is required."],
            "gender": ["This field is required."],
            "address": ["This field is required."]
        }
    }
}
```

### Duplicate Email

**Request:**
```http
POST /api/patients/
Content-Type: application/json
Authorization: Bearer <your_access_token>

{
    "name": "Bob Smith",
    "email": "alice.johnson@email.com",
    ...
}
```

**Expected Response (400 Bad Request):**
```json
{
    "success": false,
    "error": {
        "message": "Failed to create patient",
        "details": {
            "email": ["A patient with this email already exists."]
        }
    }
}
```

### Invalid Token

**Request:**
```http
GET /api/patients/
Authorization: Bearer invalid_token
```

**Expected Response (401 Unauthorized):**
```json
{
    "success": false,
    "error": {
        "message": "Given token not valid for any token type",
        "details": null
    }
}
```

### Unauthorized Access

**Request:**
```http
GET /api/patients/
```

**Expected Response (401 Unauthorized):**
```json
{
    "success": false,
    "error": {
        "message": "Authentication credentials were not provided.",
        "details": null
    }
}
```

## 6. Complete Testing Workflow

1. **Register a user** → Save user details
2. **Login** → Save access token
3. **Create multiple patients** → Save patient IDs
4. **Create multiple doctors** → Save doctor IDs
5. **Assign doctors to patients** → Create mappings
6. **Retrieve all patients** → Verify list
7. **Retrieve all doctors** → Verify list
8. **Retrieve mappings for a specific patient** → Verify assignments
9. **Update a patient's information** → Verify update
10. **Remove a doctor from a patient** → Verify removal
11. **Delete test data** → Clean up

## 7. Specialization Options for Doctors

When creating or updating a doctor, use one of these specialization values:

- `CARDIOLOGY` - Cardiology
- `DERMATOLOGY` - Dermatology
- `NEUROLOGY` - Neurology
- `ORTHOPEDICS` - Orthopedics
- `PEDIATRICS` - Pediatrics
- `GENERAL` - General Practitioner
- `OTHER` - Other

## 8. Gender Options for Patients

When creating or updating a patient, use one of these gender values:

- `M` - Male
- `F` - Female
- `O` - Other

## Tips for Testing

1. **Use a REST client**: Postman, Insomnia, or Thunder Client (VS Code extension)
2. **Save tokens**: Store the access token in your environment variables
3. **Organize requests**: Group related requests together
4. **Test validation**: Try invalid inputs to verify error handling
5. **Check status codes**: Verify correct HTTP status codes are returned
6. **Test edge cases**: Empty strings, special characters, very long inputs
7. **Test authorization**: Try accessing endpoints without tokens

## Refresh Token Example

When your access token expires:

**Request:**
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Expected Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

Use the new access token for subsequent requests.
