from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Patient, Doctor, PatientDoctorMapping


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model with validation.
    """
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'email', 'phone', 'date_of_birth', 
            'gender', 'address', 'medical_history', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def validate_email(self, value):
        # Check if email already exists (excluding current instance during update)
        instance = self.instance
        if instance:
            if Patient.objects.filter(email=value).exclude(id=instance.id).exists():
                raise serializers.ValidationError("A patient with this email already exists.")
        else:
            if Patient.objects.filter(email=value).exists():
                raise serializers.ValidationError("A patient with this email already exists.")
        return value


class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor model with validation.
    """
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'email', 'phone', 'specialization',
            'license_number', 'years_of_experience', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def validate_email(self, value):
        instance = self.instance
        if instance:
            if Doctor.objects.filter(email=value).exclude(id=instance.id).exists():
                raise serializers.ValidationError("A doctor with this email already exists.")
        else:
            if Doctor.objects.filter(email=value).exists():
                raise serializers.ValidationError("A doctor with this email already exists.")
        return value
    
    def validate_license_number(self, value):
        instance = self.instance
        if instance:
            if Doctor.objects.filter(license_number=value).exclude(id=instance.id).exists():
                raise serializers.ValidationError("A doctor with this license number already exists.")
        else:
            if Doctor.objects.filter(license_number=value).exists():
                raise serializers.ValidationError("A doctor with this license number already exists.")
        return value
    
    def validate_years_of_experience(self, value):
        if value < 0:
            raise serializers.ValidationError("Years of experience cannot be negative.")
        if value > 70:
            raise serializers.ValidationError("Years of experience seems unrealistic.")
        return value


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for PatientDoctorMapping model.
    """
    patient_details = PatientSerializer(source='patient', read_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient', 'doctor', 'patient_details', 
            'doctor_details', 'assigned_date', 'notes', 'created_by'
        ]
        read_only_fields = ['id', 'assigned_date', 'created_by']
    
    def validate(self, attrs):
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        
        # Check if mapping already exists (excluding current instance during update)
        instance = self.instance
        if instance:
            if PatientDoctorMapping.objects.filter(
                patient=patient, 
                doctor=doctor
            ).exclude(id=instance.id).exists():
                raise serializers.ValidationError(
                    "This patient is already assigned to this doctor."
                )
        else:
            if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
                raise serializers.ValidationError(
                    "This patient is already assigned to this doctor."
                )
        
        return attrs


class PatientDoctorMappingListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing mappings.
    """
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient', 'patient_name', 'doctor', 'doctor_name', 'assigned_date', 'notes']
        read_only_fields = ['id', 'assigned_date']
