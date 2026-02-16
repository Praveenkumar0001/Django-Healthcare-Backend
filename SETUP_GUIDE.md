# Quick Setup Commands for Django Healthcare Backend

## Step-by-Step Setup

### 1. Navigate to Project Directory
```powershell
cd "c:\Users\prave\OneDrive\Desktop\Django Assignment"
```

### 2. Create and Activate Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (PowerShell)
.\venv\Scripts\Activate

# OR for CMD
# venv\Scripts\activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```powershell
# Copy the example env file
copy .env.example .env

# Edit .env file with your database credentials
# Use notepad or any text editor:
notepad .env
```

Update the following in .env:
```
SECRET_KEY=django-insecure-your-secret-key-here-make-it-random-and-long
DEBUG=True
DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Setup PostgreSQL Database

Open PostgreSQL command line (psql) or pgAdmin and run:
```sql
CREATE DATABASE healthcare_db;
```

If you need to create a new user:
```sql
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO your_username;
```

### 6. Run Django Migrations
```powershell
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

### 7. Create Superuser (Optional but Recommended)
```powershell
python manage.py createsuperuser
```
Follow the prompts to create an admin user.

### 8. Run Development Server
```powershell
python manage.py runserver
```

The server will start at: http://127.0.0.1:8000/

### 9. Access Admin Panel (Optional)
Visit: http://127.0.0.1:8000/admin/
Login with superuser credentials.

### 10. Test the API

#### Option A: Using cURL (PowerShell)
```powershell
# Register a new user
curl.exe -X POST http://127.0.0.1:8000/api/auth/register/ `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"testuser\",\"email\":\"test@example.com\",\"first_name\":\"Test\",\"last_name\":\"User\",\"password\":\"TestPass123!\",\"password2\":\"TestPass123!\"}'

# Login
curl.exe -X POST http://127.0.0.1:8000/api/auth/login/ `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"testuser\",\"password\":\"TestPass123!\"}'
```

#### Option B: Using Postman or Thunder Client
1. Import requests from API_TESTING_GUIDE.md
2. Start with register and login endpoints
3. Use the access token for other endpoints

## Quick Verification Commands

### Check if Virtual Environment is Active
```powershell
# Should show the path to your venv Python
Get-Command python | Select-Object Source
```

### Check Installed Packages
```powershell
pip list
```

### Check Django Version
```powershell
python -m django --version
```

### Check Database Connection
```powershell
python manage.py dbshell
# Should connect to PostgreSQL
# Type \q to exit
```

### Run Django Check
```powershell
python manage.py check
```

### View Available URLs
```powershell
python manage.py show_urls
# If django-extensions is installed, otherwise check urls.py files
```

## Troubleshooting

### Virtual Environment Not Activating
```powershell
# If PowerShell execution policy blocks it:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### PostgreSQL Connection Error
- Verify PostgreSQL service is running
- Check credentials in .env file
- Ensure database exists
- Check if pg_hba.conf allows local connections

### Module Not Found Error
```powershell
# Ensure venv is activated
.\venv\Scripts\Activate

# Reinstall requirements
pip install -r requirements.txt
```

### Migration Errors
```powershell
# Delete all migration files except __init__.py in api/migrations/
# Then run:
python manage.py makemigrations
python manage.py migrate
```

### Port Already in Use
```powershell
# Run on different port
python manage.py runserver 8001
```

## Development Workflow

### Making Model Changes
```powershell
# 1. Edit models in api/models.py
# 2. Create migrations
python manage.py makemigrations
# 3. Apply migrations
python manage.py migrate
```

### Creating New Endpoints
```powershell
# 1. Add serializer in api/serializers.py
# 2. Add view in api/views.py
# 3. Add URL pattern in api/urls.py
# 4. Test the endpoint
```

### Running Tests (if you create them)
```powershell
python manage.py test
```

## Production Considerations

When deploying to production:

1. Set `DEBUG=False` in .env
2. Generate a strong SECRET_KEY
3. Configure ALLOWED_HOSTS in settings.py
4. Use a production-grade database
5. Set up proper CORS settings
6. Use HTTPS
7. Set up static file serving
8. Configure logging
9. Use environment-specific settings
10. Set up monitoring and backups

## Useful Django Commands

```powershell
# Create new app
python manage.py startapp appname

# Create superuser
python manage.py createsuperuser

# Change user password
python manage.py changepassword username

# Run Django shell
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic

# Show migrations
python manage.py showmigrations

# Database shell
python manage.py dbshell

# Flush database (delete all data)
python manage.py flush
```

## Git Commands (Optional)

```powershell
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Django Healthcare Backend"

# Create .gitignore (already provided)
# Ensure .env is in .gitignore before committing!
```

## Next Steps

1. ✅ Follow setup steps above
2. ✅ Test all API endpoints using API_TESTING_GUIDE.md
3. ✅ Explore admin panel
4. ✅ Create sample data
5. ✅ Test authentication flow
6. ✅ Test CRUD operations
7. ✅ Test patient-doctor mappings
8. ✅ Review error handling
9. ✅ (Optional) Write unit tests
10. ✅ (Optional) Deploy to cloud platform

## Support Resources

- Django Documentation: https://docs.djangoproject.com/
- DRF Documentation: https://www.django-rest-framework.org/
- SimpleJWT: https://django-rest-framework-simplejwt.readthedocs.io/
- PostgreSQL Documentation: https://www.postgresql.org/docs/

---

**Project Status**: ✅ Ready for Development and Testing
