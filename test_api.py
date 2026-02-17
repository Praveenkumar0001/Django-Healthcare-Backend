"""
Comprehensive API Test Script
Tests all endpoints to verify the Django Healthcare Backend is working correctly.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_response(response):
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print()

# Store tokens and IDs
tokens = {}
patient_id = None
doctor_id = None
mapping_id = None

try:
    # Test 1: Register User
    print_header("TEST 1: Register User")
    register_data = {
        "username": f"testuser_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "email": f"test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "TestPass123!",
        "password2": "TestPass123!"
    }
    response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
    print_response(response)
    
    if response.status_code != 201:
        print("❌ FAILED: User registration failed")
        exit(1)
    print("✅ PASSED: User registered successfully")
    
    # Test 2: Login User
    print_header("TEST 2: Login User")
    login_data = {
        "username": register_data["username"],
        "password": register_data["password"]
    }
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    print_response(response)
    
    if response.status_code != 200:
        print("❌ FAILED: User login failed")
        exit(1)
    
    data = response.json()
    tokens['access'] = data['data']['tokens']['access']
    tokens['refresh'] = data['data']['tokens']['refresh']
    print("✅ PASSED: User logged in successfully")
    print(f"Access Token: {tokens['access'][:50]}...")
    
    # Headers with authentication
    headers = {
        "Authorization": f"Bearer {tokens['access']}",
        "Content-Type": "application/json"
    }
    
    # Test 3: Create Patient
    print_header("TEST 3: Create Patient")
    patient_data = {
        "name": "John Doe",
        "email": f"john.doe_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-05-15",
        "gender": "M",
        "address": "123 Main St, Springfield, IL 62701",
        "medical_history": "No known allergies. Previous surgery in 2020."
    }
    response = requests.post(f"{BASE_URL}/patients/", json=patient_data, headers=headers)
    print_response(response)
    
    if response.status_code != 201:
        print("❌ FAILED: Patient creation failed")
        exit(1)
    
    patient_id = response.json()['data']['id']
    print(f"✅ PASSED: Patient created successfully (ID: {patient_id})")
    
    # Test 4: Get All Patients
    print_header("TEST 4: Get All Patients")
    response = requests.get(f"{BASE_URL}/patients/", headers=headers)
    print_response(response)
    
    if response.status_code != 200:
        print("❌ FAILED: Failed to retrieve patients")
        exit(1)
    print("✅ PASSED: Patients retrieved successfully")
    
    # Test 5: Get Specific Patient
    print_header("TEST 5: Get Specific Patient")
    response = requests.get(f"{BASE_URL}/patients/{patient_id}/", headers=headers)
    print_response(response)
    
    if response.status_code != 200:
        print("❌ FAILED: Failed to retrieve patient details")
        exit(1)
    print("✅ PASSED: Patient details retrieved successfully")
    
    # Test 6: Update Patient
    print_header("TEST 6: Update Patient (PATCH)")
    update_data = {
        "phone": "+1234567899",
        "medical_history": "Updated medical history. No known allergies."
    }
    response = requests.patch(f"{BASE_URL}/patients/{patient_id}/", json=update_data, headers=headers)
    print_response(response)
    
    if response.status_code != 200:
        print("❌ FAILED: Patient update failed")
        exit(1)
    print("✅ PASSED: Patient updated successfully")
    
    # Test 7: Create Doctor
    print_header("TEST 7: Create Doctor")
    doctor_data = {
        "name": "Dr. Sarah Johnson",
        "email": f"dr.johnson_{datetime.now().strftime('%Y%m%d%H%M%S')}@hospital.com",
        "phone": "+19876543210",
        "specialization": "CARDIOLOGY",
        "license_number": f"LIC{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "years_of_experience": 15
    }
    response = requests.post(f"{BASE_URL}/doctors/", json=doctor_data, headers=headers)
    print_response(response)
    
    if response.status_code != 201:
        print("❌ FAILED: Doctor creation failed")
        exit(1)
    
    doctor_id = response.json()['data']['id']
    print(f"✅ PASSED: Doctor created successfully (ID: {doctor_id})")
    
    # Test 8: Get All Doctors
    print_header("TEST 8: Get All Doctors")
    response = requests.get(f"{BASE_URL}/doctors/", headers=headers)
    print_response(response)
    
    if response.status_code != 200:
        print("❌ FAILED: Failed to retrieve doctors")
        exit(1)
    print("✅ PASSED: Doctors retrieved successfully")
    
    # Test 9: Get Specific Doctor
    print_header("TEST 9: Get Specific Doctor")
    response = requests.get(f"{BASE_URL}/doctors/{doctor_id}/", headers=headers)
    print_response(response)
    
    if response.status_code != 200:
        print("❌ FAILED: Failed to retrieve doctor details")
        exit(1)
    print("✅ PASSED: Doctor details retrieved successfully")
    
    # Test 10: Assign Doctor to Patient
    print_header("TEST 10: Assign Doctor to Patient")
    mapping_data = {
        "patient": patient_id,
        "doctor": doctor_id,
        "notes": "Regular cardiology checkup scheduled"
    }
    response = requests.post(f"{BASE_URL}/mappings/", json=mapping_data, headers=headers)
    print_response(response)
    
    if response.status_code != 201:
        print("❌ FAILED: Failed to assign doctor to patient")
        exit(1)
    
    mapping_id = response.json()['data']['id']
    print(f"✅ PASSED: Doctor assigned to patient successfully (Mapping ID: {mapping_id})")
    
    # Test 11: Get All Mappings
    print_header("TEST 11: Get All Mappings")
    response = requests.get(f"{BASE_URL}/mappings/", headers=headers)
    print_response(response)
    
    if response.status_code != 200:
        print("❌ FAILED: Failed to retrieve mappings")
        exit(1)
    print("✅ PASSED: Mappings retrieved successfully")
    
    # Test 12: Get Doctors for Specific Patient
    print_header("TEST 12: Get Doctors for Specific Patient")
    response = requests.get(f"{BASE_URL}/mappings/?patient_id={patient_id}", headers=headers)
    print_response(response)
    
    if response.status_code != 200:
        print("❌ FAILED: Failed to retrieve patient's doctors")
        exit(1)
    print("✅ PASSED: Patient's doctors retrieved successfully")
    
    # Test 13: Test Authentication (Access without token)
    print_header("TEST 13: Test Authentication (Should Fail)")
    response = requests.get(f"{BASE_URL}/patients/")
    print_response(response)
    
    if response.status_code != 401:
        print("❌ FAILED: Endpoint should require authentication")
        exit(1)
    print("✅ PASSED: Authentication required (as expected)")
    
    # Test 14: Refresh Token
    print_header("TEST 14: Refresh Access Token")
    refresh_data = {
        "refresh": tokens['refresh']
    }
    response = requests.post(f"{BASE_URL}/auth/token/refresh/", json=refresh_data)
    print_response(response)
    
    if response.status_code != 200:
        print("❌ FAILED: Token refresh failed")
        exit(1)
    print("✅ PASSED: Token refreshed successfully")
    
    # Test 15: Delete Mapping
    print_header("TEST 15: Delete Doctor-Patient Mapping")
    response = requests.delete(f"{BASE_URL}/mappings/{mapping_id}/", headers=headers)
    print_response(response)
    
    if response.status_code != 200:
        print("❌ FAILED: Failed to delete mapping")
        exit(1)
    print("✅ PASSED: Mapping deleted successfully")
    
    # Test 16: Delete Patient
    print_header("TEST 16: Delete Patient")
    response = requests.delete(f"{BASE_URL}/patients/{patient_id}/", headers=headers)
    print_response(response)
    
    if response.status_code != 200:
        print("❌ FAILED: Failed to delete patient")
        exit(1)
    print("✅ PASSED: Patient deleted successfully")
    
    # Test 17: Delete Doctor
    print_header("TEST 17: Delete Doctor")
    response = requests.delete(f"{BASE_URL}/doctors/{doctor_id}/", headers=headers)
    print_response(response)
    
    if response.status_code != 200:
        print("❌ FAILED: Failed to delete doctor")
        exit(1)
    print("✅ PASSED: Doctor deleted successfully")
    
    # Final Summary
    print_header("🎉 ALL TESTS PASSED!")
    print("✅ User Registration - Working")
    print("✅ User Login - Working")
    print("✅ JWT Authentication - Working")
    print("✅ Patient CRUD - Working")
    print("✅ Doctor CRUD - Working")
    print("✅ Patient-Doctor Mapping - Working")
    print("✅ Authorization - Working")
    print("✅ Token Refresh - Working")
    print("\n🚀 Django Healthcare Backend is fully functional!")
    
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: Cannot connect to server!")
    print("Make sure the Django server is running:")
    print("Run: python manage.py runserver")
    exit(1)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)
