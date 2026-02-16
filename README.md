# Django Healthcare Backend

A robust healthcare backend system built with Django, Django REST Framework, and PostgreSQL. This application provides secure APIs for managing patient and doctor records with JWT authentication.

## Features

- **JWT Authentication** - Secure user registration and login
- **Patient Management** - Complete CRUD operations for patient records
- **Doctor Management** - Complete CRUD operations for doctor records
- **Patient-Doctor Mapping** - Assign doctors to patients and manage relationships
- **PostgreSQL Database** - Reliable data storage
- **Error Handling & Validation** - Comprehensive input validation and error responses
- **Environment Variables** - Secure configuration management

## Technology Stack

- **Backend Framework**: Django 4.2.9
- **API Framework**: Django REST Framework 3.14.0
- **Authentication**: djangorestframework-simplejwt 5.3.1
- **Database**: PostgreSQL (with psycopg2-binary 2.9.9)
- **Configuration**: python-decouple 3.8
- **CORS**: django-cors-headers 4.3.1

## Project Structure

```
Django Assignment/
├── healthcare_backend/          # Main project directory
│   ├── __init__.py
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Main URL configuration
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
├── api/                        # API application
│   ├── __init__.py
│   ├── models.py               # Database models
│   ├── serializers.py          # DRF serializers
│   ├── views.py                # API views
│   ├── urls.py                 # API URL routing
│   ├── admin.py                # Admin configuration
│   ├── apps.py                 # App configuration
│   └── utils.py                # Utility functions
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Step 1: Clone/Setup the Project

```bash
cd "c:\Users\prave\OneDrive\Desktop\Django Assignment"
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate
```

**Windows (CMD):**
```cmd
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure PostgreSQL Database

1. Create a PostgreSQL database:

```sql
CREATE DATABASE healthcare_db;
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO your_username;
```

2. Create `.env` file from `.env.example`:

```bash
# Copy the example file
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux
```

3. Update `.env` with your database credentials:

```env
SECRET_KEY=your-secret-key-here-generate-a-strong-one
DEBUG=True
DB_NAME=healthcare_db
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

## API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

### Authentication Endpoints

#### 1. Register User
- **URL**: `/api/auth/register/`
- **Method**: `POST`
- **Auth Required**: No
- **Request Body**:
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
}
```
- **Success Response** (201):
```json
{
    "success": true,
    "message": "User registered successfully",
    "data": {
        "user": {
            "id": 1,
            "username": "johndoe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }
    }
}
```

#### 2. Login User
- **URL**: `/api/auth/login/`
- **Method**: `POST`
- **Auth Required**: No
- **Request Body**:
```json
{
    "username": "johndoe",
    "password": "SecurePass123!"
}
```
- **Success Response** (200):
```json
{
    "success": true,
    "message": "Login successful",
    "data": {
        "user": {
            "id": 1,
            "username": "johndoe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe"
        },
        "tokens": {
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
            "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
        }
    }
}
```

#### 3. Refresh Token
- **URL**: `/api/auth/token/refresh/`
- **Method**: `POST`
- **Auth Required**: No
- **Request Body**:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Patient Management Endpoints

**Note**: All patient endpoints require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

#### 1. Create Patient
- **URL**: `/api/patients/`
- **Method**: `POST`
- **Request Body**:
```json
{
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "+1234567890",
    "date_of_birth": "1990-05-15",
    "gender": "F",
    "address": "123 Main St, City, State 12345",
    "medical_history": "No known allergies"
}
```
- **Success Response** (201)

#### 2. Get All Patients
- **URL**: `/api/patients/`
- **Method**: `GET`
- **Success Response** (200): Returns list of patients created by authenticated user

#### 3. Get Patient Details
- **URL**: `/api/patients/<id>/`
- **Method**: `GET`
- **Success Response** (200): Returns patient details

#### 4. Update Patient
- **URL**: `/api/patients/<id>/`
- **Method**: `PUT` or `PATCH`
- **Request Body**: Same as create (PUT requires all fields, PATCH allows partial updates)
- **Success Response** (200)

#### 5. Delete Patient
- **URL**: `/api/patients/<id>/`
- **Method**: `DELETE`
- **Success Response** (200)

### Doctor Management Endpoints

**Note**: All doctor endpoints require authentication.

#### 1. Create Doctor
- **URL**: `/api/doctors/`
- **Method**: `POST`
- **Request Body**:
```json
{
    "name": "Dr. James Wilson",
    "email": "dr.wilson@hospital.com",
    "phone": "+1234567891",
    "specialization": "CARDIOLOGY",
    "license_number": "LIC123456",
    "years_of_experience": 15
}
```
- **Specialization Options**: 
  - `CARDIOLOGY`, `DERMATOLOGY`, `NEUROLOGY`, `ORTHOPEDICS`, `PEDIATRICS`, `GENERAL`, `OTHER`
- **Success Response** (201)

#### 2. Get All Doctors
- **URL**: `/api/doctors/`
- **Method**: `GET`
- **Success Response** (200): Returns list of all doctors

#### 3. Get Doctor Details
- **URL**: `/api/doctors/<id>/`
- **Method**: `GET`
- **Success Response** (200)

#### 4. Update Doctor
- **URL**: `/api/doctors/<id>/`
- **Method**: `PUT` or `PATCH`
- **Success Response** (200)

#### 5. Delete Doctor
- **URL**: `/api/doctors/<id>/`
- **Method**: `DELETE`
- **Success Response** (200)

### Patient-Doctor Mapping Endpoints

**Note**: All mapping endpoints require authentication.

#### 1. Assign Doctor to Patient
- **URL**: `/api/mappings/`
- **Method**: `POST`
- **Request Body**:
```json
{
    "patient": 1,
    "doctor": 2,
    "notes": "Regular checkup scheduled"
}
```
- **Success Response** (201)

#### 2. Get All Mappings
- **URL**: `/api/mappings/`
- **Method**: `GET`
- **Success Response** (200): Returns all patient-doctor mappings

#### 3. Get Doctors for Specific Patient
- **URL**: `/api/mappings/?patient_id=<patient_id>`
- **Method**: `GET`
- **Success Response** (200): Returns all doctors assigned to the specified patient

#### 4. Remove Doctor from Patient
- **URL**: `/api/mappings/<id>/`
- **Method**: `DELETE`
- **Success Response** (200)

## Data Models

### Patient Model
- `name` - CharField (max 200)
- `email` - EmailField (unique)
- `phone` - CharField (validated format)
- `date_of_birth` - DateField
- `gender` - CharField (M/F/O)
- `address` - TextField
- `medical_history` - TextField (optional)
- `created_by` - ForeignKey to User
- `created_at` - DateTimeField (auto)
- `updated_at` - DateTimeField (auto)

### Doctor Model
- `name` - CharField (max 200)
- `email` - EmailField (unique)
- `phone` - CharField (validated format)
- `specialization` - CharField (choices)
- `license_number` - CharField (unique)
- `years_of_experience` - IntegerField
- `created_by` - ForeignKey to User
- `created_at` - DateTimeField (auto)
- `updated_at` - DateTimeField (auto)

### PatientDoctorMapping Model
- `patient` - ForeignKey to Patient
- `doctor` - ForeignKey to Doctor
- `assigned_date` - DateTimeField (auto)
- `notes` - TextField (optional)
- `created_by` - ForeignKey to User
- Unique constraint on (patient, doctor) pair

## Error Handling

All API responses follow a consistent format:

**Success Response:**
```json
{
    "success": true,
    "message": "Operation successful",
    "data": { ... }
}
```

**Error Response:**
```json
{
    "success": false,
    "error": {
        "message": "Error description",
        "details": { ... }
    }
}
```

## Testing the API

### Using cURL

**Register a user:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"email\":\"test@example.com\",\"first_name\":\"Test\",\"last_name\":\"User\",\"password\":\"TestPass123!\",\"password2\":\"TestPass123!\"}"
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"password\":\"TestPass123!\"}"
```

**Create a patient (replace TOKEN with your access token):**
```bash
curl -X POST http://127.0.0.1:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d "{\"name\":\"John Patient\",\"email\":\"patient@example.com\",\"phone\":\"+1234567890\",\"date_of_birth\":\"1990-01-01\",\"gender\":\"M\",\"address\":\"123 Street\"}"
```

### Using Postman

1. Import the project as a collection
2. Create an environment with `base_url` = `http://127.0.0.1:8000`
3. Register and login to get an access token
4. Set the token in the Authorization header for protected endpoints

## Security Features

- JWT-based authentication
- Password validation (Django's built-in validators)
- CORS headers configuration
- Environment-based configuration
- Unique constraints on emails and license numbers
- User-specific data access for patients

## Admin Panel

Access the Django admin panel at `http://127.0.0.1:8000/admin/`

Use the superuser credentials created earlier to:
- View and manage users
- View and manage patients, doctors, and mappings
- Access detailed records with search and filtering

## Environment Variables

Required environment variables (create a `.env` file):

```env
SECRET_KEY=<your-secret-key>
DEBUG=True/False
DB_NAME=<database-name>
DB_USER=<database-user>
DB_PASSWORD=<database-password>
DB_HOST=<database-host>
DB_PORT=<database-port>
```

## Common Issues & Solutions

### Issue: Database connection error
**Solution**: Verify PostgreSQL is running and credentials in `.env` are correct

### Issue: Module not found
**Solution**: Ensure virtual environment is activated and dependencies are installed

### Issue: Migration errors
**Solution**: Delete migration files (except `__init__.py`) and run `makemigrations` again

### Issue: JWT token expired
**Solution**: Use the refresh token endpoint to get a new access token

## Development Notes

- Always activate the virtual environment before running commands
- Run `python manage.py makemigrations` after model changes
- Keep `.env` file secure and never commit it to version control
- Use `DEBUG=False` in production

## License

This project is for educational purposes as part of a Django assignment.

## Author

Built as part of the Django Healthcare Backend Assignment

## Support

For issues or questions, please refer to the Django and DRF documentation:
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [SimpleJWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/)
