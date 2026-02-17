import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_backend.settings')
django.setup()

from django.db import connection

try:
    # Test database connection
    connection.ensure_connection()
    
    print("="*60)
    print("✅ DATABASE CONNECTION SUCCESSFUL!")
    print("="*60)
    print(f"\nDatabase Engine: {connection.settings_dict['ENGINE']}")
    print(f"Database Name: {connection.settings_dict['NAME']}")
    print(f"Database User: {connection.settings_dict['USER']}")
    print(f"Database Host: {connection.settings_dict['HOST']}")
    print(f"Database Port: {connection.settings_dict['PORT']}")
    
    # Get PostgreSQL version
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"\nPostgreSQL Version: {version.split(',')[0]}")
        
        # Count tables
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
        table_count = cursor.fetchone()[0]
        print(f"Total Tables: {table_count}")
        
        # List our custom tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE 'api_%'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"\nCustom API Tables:")
        for table in tables:
            print(f"  - {table[0]}")
    
    print("\n" + "="*60)
    print("✅ All database checks passed!")
    print("="*60)
    
except Exception as e:
    print("="*60)
    print("❌ DATABASE CONNECTION FAILED!")
    print("="*60)
    print(f"\nError: {str(e)}")
    print("\nPlease check:")
    print("1. PostgreSQL server is running")
    print("2. Database 'healthcare_db' exists")
    print("3. Credentials in .env file are correct")
    print("4. PostgreSQL is accepting connections on localhost:5432")
