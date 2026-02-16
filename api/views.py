from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q

from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    UserRegistrationSerializer,
    PatientSerializer,
    DoctorSerializer,
    PatientDoctorMappingSerializer,
    PatientDoctorMappingListSerializer
)
from .utils import success_response, error_response


# ==================== Authentication Views ====================

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user.
    POST /api/auth/register/
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return success_response(
            data={
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            },
            message="User registered successfully",
            status_code=status.HTTP_201_CREATED
        )
    return error_response(
        message="Registration failed",
        details=serializer.errors,
        status_code=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Login user and return JWT tokens.
    POST /api/auth/login/
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return error_response(
            message="Please provide both username and password",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return success_response(
            data={
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            },
            message="Login successful"
        )
    
    return error_response(
        message="Invalid credentials",
        status_code=status.HTTP_401_UNAUTHORIZED
    )


# ==================== Patient ViewSet ====================

class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patients.
    Provides CRUD operations for patient records.
    """
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return patients created by the authenticated user.
        """
        return Patient.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        """
        Save the patient with the current user as creator.
        """
        serializer.save(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return success_response(
                data=serializer.data,
                message="Patient created successfully",
                status_code=status.HTTP_201_CREATED
            )
        return error_response(
            message="Failed to create patient",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message="Patients retrieved successfully"
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(
            data=serializer.data,
            message="Patient details retrieved successfully"
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return success_response(
                data=serializer.data,
                message="Patient updated successfully"
            )
        return error_response(
            message="Failed to update patient",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(
            message="Patient deleted successfully",
            status_code=status.HTTP_200_OK
        )


# ==================== Doctor ViewSet ====================

class DoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing doctors.
    Provides CRUD operations for doctor records.
    """
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return all doctors (not filtered by user for broader access).
        """
        return Doctor.objects.all()
    
    def perform_create(self, serializer):
        """
        Save the doctor with the current user as creator.
        """
        serializer.save(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return success_response(
                data=serializer.data,
                message="Doctor created successfully",
                status_code=status.HTTP_201_CREATED
            )
        return error_response(
            message="Failed to create doctor",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message="Doctors retrieved successfully"
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(
            data=serializer.data,
            message="Doctor details retrieved successfully"
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return success_response(
                data=serializer.data,
                message="Doctor updated successfully"
            )
        return error_response(
            message="Failed to update doctor",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(
            message="Doctor deleted successfully",
            status_code=status.HTTP_200_OK
        )


# ==================== Patient-Doctor Mapping ViewSet ====================

class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patient-doctor mappings.
    Allows assigning doctors to patients.
    """
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return mappings, optionally filtered by patient_id.
        """
        queryset = PatientDoctorMapping.objects.all()
        patient_id = self.request.query_params.get('patient_id', None)
        
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        return queryset
    
    def get_serializer_class(self):
        """
        Use different serializers for list and detail views.
        """
        if self.action == 'list':
            return PatientDoctorMappingListSerializer
        return PatientDoctorMappingSerializer
    
    def perform_create(self, serializer):
        """
        Save the mapping with the current user as creator.
        """
        serializer.save(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return success_response(
                data=serializer.data,
                message="Doctor assigned to patient successfully",
                status_code=status.HTTP_201_CREATED
            )
        return error_response(
            message="Failed to assign doctor to patient",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        patient_id = request.query_params.get('patient_id', None)
        if patient_id:
            message = f"Doctors assigned to patient retrieved successfully"
        else:
            message = "All patient-doctor mappings retrieved successfully"
        
        return success_response(
            data=serializer.data,
            message=message
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(
            data=serializer.data,
            message="Mapping details retrieved successfully"
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(
            message="Doctor removed from patient successfully",
            status_code=status.HTTP_200_OK
        )
