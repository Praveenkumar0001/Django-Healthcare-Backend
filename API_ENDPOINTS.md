# API Endpoints Summary

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication: JWT Bearer Token
All endpoints except authentication require:
```
Authorization: Bearer <access_token>
```

---

## 📋 ENDPOINTS OVERVIEW

### 1. AUTHENTICATION (Public - No Auth Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register/` | Register a new user |
| POST | `/auth/login/` | Login and get JWT tokens |
| POST | `/auth/token/refresh/` | Refresh access token |

---

### 2. PATIENT MANAGEMENT (Auth Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/patients/` | Create a new patient |
| GET | `/patients/` | Get all patients (created by authenticated user) |
| GET | `/patients/<id>/` | Get specific patient details |
| PUT | `/patients/<id>/` | Update patient (full update) |
| PATCH | `/patients/<id>/` | Update patient (partial update) |
| DELETE | `/patients/<id>/` | Delete a patient |

---

### 3. DOCTOR MANAGEMENT (Auth Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/doctors/` | Create a new doctor |
| GET | `/doctors/` | Get all doctors |
| GET | `/doctors/<id>/` | Get specific doctor details |
| PUT | `/doctors/<id>/` | Update doctor (full update) |
| PATCH | `/doctors/<id>/` | Update doctor (partial update) |
| DELETE | `/doctors/<id>/` | Delete a doctor |

---

### 4. PATIENT-DOCTOR MAPPING (Auth Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/mappings/` | Assign a doctor to a patient |
| GET | `/mappings/` | Get all patient-doctor mappings |
| GET | `/mappings/?patient_id=<id>` | Get all doctors assigned to a specific patient |
| GET | `/mappings/<id>/` | Get specific mapping details |
| DELETE | `/mappings/<id>/` | Remove doctor from patient |

---

## 🔐 AUTHENTICATION DETAILS

### Register User
```http
POST /api/auth/register/
```
**Body:**
```json
{
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "password": "string",
    "password2": "string"
}
```

### Login
```http
POST /api/auth/login/
```
**Body:**
```json
{
    "username": "string",
    "password": "string"
}
```
**Returns:** Access token (valid for 5 hours) and Refresh token (valid for 1 day)

### Refresh Token
```http
POST /api/auth/token/refresh/
```
**Body:**
```json
{
    "refresh": "string"
}
```
**Returns:** New access token

---

## 👥 PATIENT FIELDS

### Required Fields:
- `name` (string, max 200 chars)
- `email` (string, valid email, unique)
- `phone` (string, format: +999999999)
- `date_of_birth` (date, format: YYYY-MM-DD)
- `gender` (string, choices: M/F/O)
- `address` (text)

### Optional Fields:
- `medical_history` (text)

### Auto-generated Fields:
- `id` (integer, auto)
- `created_by` (user object, auto)
- `created_at` (datetime, auto)
- `updated_at` (datetime, auto)

---

## 👨‍⚕️ DOCTOR FIELDS

### Required Fields:
- `name` (string, max 200 chars)
- `email` (string, valid email, unique)
- `phone` (string, format: +999999999)
- `specialization` (string, choices below)
- `license_number` (string, max 50 chars, unique)
- `years_of_experience` (integer, 0-70)

### Specialization Choices:
- `CARDIOLOGY`
- `DERMATOLOGY`
- `NEUROLOGY`
- `ORTHOPEDICS`
- `PEDIATRICS`
- `GENERAL`
- `OTHER`

### Auto-generated Fields:
- `id` (integer, auto)
- `created_by` (user object, auto)
- `created_at` (datetime, auto)
- `updated_at` (datetime, auto)

---

## 🔗 MAPPING FIELDS

### Required Fields:
- `patient` (integer, patient ID)
- `doctor` (integer, doctor ID)

### Optional Fields:
- `notes` (text)

### Auto-generated Fields:
- `id` (integer, auto)
- `assigned_date` (datetime, auto)
- `created_by` (user object, auto)

### Constraints:
- Unique combination of (patient, doctor) - cannot assign same doctor to same patient twice

---

## 📊 RESPONSE FORMAT

### Success Response:
```json
{
    "success": true,
    "message": "Operation successful",
    "data": { ... }
}
```

### Error Response:
```json
{
    "success": false,
    "error": {
        "message": "Error description",
        "details": { ... }
    }
}
```

---

## 🔍 QUERY PARAMETERS

### Filter Mappings by Patient:
```http
GET /api/mappings/?patient_id=1
```
Returns all doctors assigned to patient with ID 1.

---

## 📝 HTTP STATUS CODES

| Code | Description |
|------|-------------|
| 200 | OK - Successful GET, PUT, PATCH, DELETE |
| 201 | Created - Successful POST |
| 400 | Bad Request - Validation error |
| 401 | Unauthorized - Missing/invalid token |
| 403 | Forbidden - No permission |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

---

## ⚡ QUICK START EXAMPLES

### 1. Register & Login
```bash
# Register
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","first_name":"Test","last_name":"User","password":"TestPass123!","password2":"TestPass123!"}'

# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123!"}'
```

### 2. Create Patient
```bash
curl -X POST http://127.0.0.1:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name":"John Doe","email":"john@example.com","phone":"+1234567890","date_of_birth":"1990-01-01","gender":"M","address":"123 Street"}'
```

### 3. Create Doctor
```bash
curl -X POST http://127.0.0.1:8000/api/doctors/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name":"Dr. Smith","email":"dr.smith@hospital.com","phone":"+1234567891","specialization":"CARDIOLOGY","license_number":"LIC123","years_of_experience":15}'
```

### 4. Assign Doctor to Patient
```bash
curl -X POST http://127.0.0.1:8000/api/mappings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"patient":1,"doctor":1,"notes":"Regular checkup"}'
```

---

## 🛡️ SECURITY FEATURES

- ✅ JWT-based authentication
- ✅ Password validation (Django built-in)
- ✅ Unique email constraints
- ✅ User-specific patient access
- ✅ Environment-based configuration
- ✅ CORS headers support
- ✅ Input validation
- ✅ SQL injection protection (Django ORM)

---

## 📦 ADMIN PANEL

Access: `http://127.0.0.1:8000/admin/`

Features:
- User management
- Patient management
- Doctor management
- Mapping management
- Search and filtering
- Bulk actions

---

## 🧪 VALIDATION RULES

### Email:
- Must be valid email format
- Must be unique for patients and doctors

### Phone:
- Format: +999999999 (up to 15 digits)
- Can start with optional +

### Password:
- Minimum 8 characters
- Cannot be too similar to username
- Cannot be a commonly used password
- Cannot be entirely numeric

### License Number:
- Maximum 50 characters
- Must be unique

### Years of Experience:
- Must be between 0 and 70
- Cannot be negative

### Patient-Doctor Mapping:
- Each patient-doctor pair must be unique
- Patient and doctor must exist

---

## 🔄 COMMON WORKFLOWS

### Complete User Flow:
1. Register user → Get user details
2. Login → Get access & refresh tokens
3. Create patients → Get patient IDs
4. Create doctors → Get doctor IDs
5. Create mappings → Assign doctors to patients
6. Retrieve mappings → View assignments
7. Update records → Modify as needed
8. Delete mappings → Remove assignments
9. Delete records → Clean up

### Token Refresh Flow:
1. Access token expires (after 5 hours)
2. Use refresh token to get new access token
3. Continue using new access token
4. Refresh token valid for 1 day

---

## 📞 SUPPORT

For detailed request/response examples, see:
- `API_TESTING_GUIDE.md` - Comprehensive testing examples
- `README.md` - Project documentation
- `SETUP_GUIDE.md` - Setup instructions

---

**Last Updated:** February 16, 2026
**API Version:** 1.0
**Django Version:** 4.2.9
**DRF Version:** 3.14.0
