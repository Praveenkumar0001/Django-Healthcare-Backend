# Django Healthcare Backend - Project Structure

```
Django Assignment/
│
├── 📁 healthcare_backend/              # Main Django Project Directory
│   ├── __init__.py                     # Python package initializer
│   ├── settings.py                     # Django settings (DB, Apps, Middleware, JWT, REST Framework)
│   ├── urls.py                         # Main URL configuration (routes to admin and api)
│   ├── wsgi.py                         # WSGI configuration for deployment
│   └── asgi.py                         # ASGI configuration for async support
│
├── 📁 api/                             # Main API Application
│   ├── __init__.py                     # Python package initializer
│   ├── apps.py                         # App configuration
│   ├── admin.py                        # Django admin panel configuration
│   │                                   # - PatientAdmin
│   │                                   # - DoctorAdmin
│   │                                   # - PatientDoctorMappingAdmin
│   │
│   ├── models.py                       # Database Models
│   │   ├── Patient                     # Patient information model
│   │   ├── Doctor                      # Doctor information model
│   │   └── PatientDoctorMapping        # Many-to-many relationship model
│   │
│   ├── serializers.py                  # DRF Serializers (validation & transformation)
│   │   ├── UserRegistrationSerializer  # User registration with validation
│   │   ├── UserSerializer              # User details
│   │   ├── PatientSerializer           # Patient CRUD operations
│   │   ├── DoctorSerializer            # Doctor CRUD operations
│   │   ├── PatientDoctorMappingSerializer
│   │   └── PatientDoctorMappingListSerializer
│   │
│   ├── views.py                        # API Views
│   │   ├── register_user()             # POST /auth/register/
│   │   ├── login_user()                # POST /auth/login/
│   │   ├── PatientViewSet              # Patient CRUD endpoints
│   │   ├── DoctorViewSet               # Doctor CRUD endpoints
│   │   └── PatientDoctorMappingViewSet # Mapping CRUD endpoints
│   │
│   ├── urls.py                         # API URL routing
│   │   ├── /auth/register/             # User registration
│   │   ├── /auth/login/                # User login
│   │   ├── /auth/token/refresh/        # Refresh JWT token
│   │   ├── /patients/                  # Patient endpoints
│   │   ├── /doctors/                   # Doctor endpoints
│   │   └── /mappings/                  # Mapping endpoints
│   │
│   └── utils.py                        # Utility Functions
│       ├── custom_exception_handler()  # Custom error handling
│       ├── success_response()          # Standardized success responses
│       └── error_response()            # Standardized error responses
│
├── 📄 manage.py                        # Django management script
│
├── 📄 requirements.txt                 # Python dependencies
│   ├── Django==4.2.9
│   ├── djangorestframework==3.14.0
│   ├── djangorestframework-simplejwt==5.3.1
│   ├── psycopg2-binary==2.9.9
│   ├── python-decouple==3.8
│   └── django-cors-headers==4.3.1
│
├── 📄 .env.example                     # Environment variables template
│   ├── SECRET_KEY                      # Django secret key
│   ├── DEBUG                           # Debug mode flag
│   ├── DB_NAME                         # PostgreSQL database name
│   ├── DB_USER                         # Database user
│   ├── DB_PASSWORD                     # Database password
│   ├── DB_HOST                         # Database host
│   └── DB_PORT                         # Database port
│
├── 📄 .env                             # Actual environment variables (not in git)
├── 📄 .gitignore                       # Git ignore rules
│
├── 📄 README.md                        # Main project documentation
│   ├── Features overview
│   ├── Technology stack
│   ├── Installation instructions
│   ├── API documentation
│   ├── Database models
│   ├── Testing guide
│   └── Troubleshooting
│
├── 📄 API_TESTING_GUIDE.md            # Comprehensive API testing examples
│   ├── Complete request/response examples
│   ├── All endpoints with sample data
│   ├── Error scenarios
│   └── Testing workflow
│
├── 📄 API_ENDPOINTS.md                # Quick API reference
│   ├── Endpoints summary table
│   ├── Field descriptions
│   ├── Query parameters
│   └── Quick examples
│
└── 📄 SETUP_GUIDE.md                  # Step-by-step setup instructions
    ├── PowerShell commands
    ├── Database setup
    ├── Troubleshooting tips
    └── Development workflow
```

## 🗃️ Database Schema

```
┌─────────────────────┐
│       User          │  (Django built-in)
│─────────────────────│
│ id                  │
│ username            │
│ email               │
│ password            │
│ first_name          │
│ last_name           │
└─────────────────────┘
          │
          │ created_by (FK)
          ├─────────────────────────────────┐
          │                                 │
          ↓                                 ↓
┌─────────────────────┐         ┌─────────────────────┐
│      Patient        │         │       Doctor        │
│─────────────────────│         │─────────────────────│
│ id (PK)             │         │ id (PK)             │
│ name                │         │ name                │
│ email (unique)      │         │ email (unique)      │
│ phone               │         │ phone               │
│ date_of_birth       │         │ specialization      │
│ gender              │         │ license_number      │
│ address             │         │ years_of_experience │
│ medical_history     │         │ created_by (FK)     │
│ created_by (FK)     │         │ created_at          │
│ created_at          │         │ updated_at          │
│ updated_at          │         └─────────────────────┘
└─────────────────────┘                    │
          │                                │
          │                                │
          └────────────┬───────────────────┘
                       │
                       ↓
            ┌─────────────────────────┐
            │ PatientDoctorMapping    │
            │─────────────────────────│
            │ id (PK)                 │
            │ patient (FK)            │
            │ doctor (FK)             │
            │ assigned_date           │
            │ notes                   │
            │ created_by (FK)         │
            │─────────────────────────│
            │ UNIQUE(patient, doctor) │
            └─────────────────────────┘
```

## 🔄 Application Flow

```
1. USER REGISTRATION & AUTHENTICATION
   ↓
   Register User → User Model Created
   ↓
   Login → JWT Token Generated (Access + Refresh)
   ↓
   Use Access Token for API Requests

2. PATIENT MANAGEMENT
   ↓
   Create Patient → Patient Model Created (linked to User)
   ↓
   View/Update/Delete Patients (filtered by creator)

3. DOCTOR MANAGEMENT
   ↓
   Create Doctor → Doctor Model Created (linked to User)
   ↓
   View/Update/Delete Doctors (accessible by all authenticated users)

4. PATIENT-DOCTOR ASSIGNMENT
   ↓
   Create Mapping → PatientDoctorMapping Created
   ↓
   View Mappings → List all or filter by patient
   ↓
   Delete Mapping → Remove assignment
```

## 🔐 Authentication Flow

```
User
  ↓
  Register → POST /api/auth/register/
  ↓
  User Created in Database
  ↓
  Login → POST /api/auth/login/
  ↓
  Django Authenticate
  ↓
  Generate JWT Tokens (Access + Refresh)
  ↓
  Return Tokens to User
  ↓
  User includes Access Token in subsequent requests
  ↓
  JWT Authentication Middleware validates token
  ↓
  If valid → Process request
  If invalid → Return 401 Unauthorized
  If expired → Use refresh token to get new access token
```

## 📊 API Request/Response Flow

```
Client Request
  ↓
  Django Middleware (CORS, Authentication)
  ↓
  URL Router (healthcare_backend/urls.py → api/urls.py)
  ↓
  View Function/ViewSet
  ↓
  Permission Check (IsAuthenticated)
  ↓
  Serializer Validation
  ↓
  Database Operation (via Django ORM)
  ↓
  Serializer Response Formation
  ↓
  Custom Response Handler (success_response/error_response)
  ↓
  JSON Response to Client
```

## 🛠️ Key Technologies & Their Roles

```
┌──────────────────────────────────────────────────────────┐
│                        CLIENT                            │
│         (Postman, Browser, Mobile App, etc.)             │
└───────────────────────┬──────────────────────────────────┘
                        │ HTTP/HTTPS
                        ↓
┌──────────────────────────────────────────────────────────┐
│                   DJANGO REST FRAMEWORK                  │
│  ┌────────────────────────────────────────────────────┐  │
│  │  REST API Layer                                    │  │
│  │  - Serializers (Data Validation & Transformation) │  │
│  │  - ViewSets (CRUD Logic)                          │  │
│  │  - Routers (URL Generation)                       │  │
│  └────────────────────────────────────────────────────┘  │
└───────────────────────┬──────────────────────────────────┘
                        │
                        ↓
┌──────────────────────────────────────────────────────────┐
│              DJANGORESTFRAMEWORK-SIMPLEJWT               │
│  ┌────────────────────────────────────────────────────┐  │
│  │  JWT Authentication                                │  │
│  │  - Token Generation                                │  │
│  │  - Token Validation                                │  │
│  │  - Token Refresh                                   │  │
│  └────────────────────────────────────────────────────┘  │
└───────────────────────┬──────────────────────────────────┘
                        │
                        ↓
┌──────────────────────────────────────────────────────────┐
│                      DJANGO CORE                         │
│  ┌────────────────────────────────────────────────────┐  │
│  │  - ORM (Database Abstraction)                      │  │
│  │  - Models (Data Structure)                         │  │
│  │  - Admin Panel                                     │  │
│  │  - Middleware                                      │  │
│  │  - Settings Management                             │  │
│  └────────────────────────────────────────────────────┘  │
└───────────────────────┬──────────────────────────────────┘
                        │
                        ↓
┌──────────────────────────────────────────────────────────┐
│                   PSYCOPG2 (Database Driver)             │
└───────────────────────┬──────────────────────────────────┘
                        │
                        ↓
┌──────────────────────────────────────────────────────────┐
│                    POSTGRESQL DATABASE                   │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Tables:                                           │  │
│  │  - auth_user                                       │  │
│  │  - api_patient                                     │  │
│  │  - api_doctor                                      │  │
│  │  - api_patientdoctormapping                        │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

## 📁 File Dependencies

```
manage.py
  └── imports → healthcare_backend.settings

healthcare_backend/settings.py
  └── imports → decouple (for .env)
  └── configures → INSTALLED_APPS
      ├── rest_framework
      ├── rest_framework_simplejwt
      ├── corsheaders
      └── api

healthcare_backend/urls.py
  └── includes → api.urls

api/urls.py
  └── imports → api.views
      ├── register_user
      ├── login_user
      ├── PatientViewSet
      ├── DoctorViewSet
      └── PatientDoctorMappingViewSet

api/views.py
  └── imports → api.serializers
  └── imports → api.models
  └── imports → api.utils

api/serializers.py
  └── imports → api.models

api/models.py
  └── imports → django.db.models
  └── imports → django.contrib.auth.models.User
```

## 🎯 Features Implementation Map

```
REQUIREMENT                          IMPLEMENTATION
─────────────────────────────────────────────────────────────
✅ Django & DRF                    → settings.py, requirements.txt
✅ PostgreSQL                       → settings.py DATABASES config
✅ JWT Authentication               → rest_framework_simplejwt
✅ RESTful API Endpoints            → ViewSets in views.py
✅ Django ORM                       → models.py (Patient, Doctor, Mapping)
✅ Error Handling & Validation      → serializers.py, utils.py
✅ Environment Variables            → .env, python-decouple
✅ User Registration                → register_user view
✅ User Login                       → login_user view
✅ Patient CRUD                     → PatientViewSet
✅ Doctor CRUD                      → DoctorViewSet
✅ Patient-Doctor Mapping           → PatientDoctorMappingViewSet
✅ Secure Authentication            → JWT tokens, permissions
✅ Best Practices                   → Project structure, documentation
```

---

**This structure ensures:**
- ✅ Separation of concerns
- ✅ Scalability
- ✅ Maintainability
- ✅ Security
- ✅ Testability
- ✅ Clear documentation
