#🧱 4.1 Create serializers.py inside core/

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Appointment, Prescription, FileUpload
from django.utils import timezone

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role  # Assuming you have a 'role' field
        return token
    
#👤 4.2 User Serializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

#📅 4.3 Appointment Serializer

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.username', read_only=True)
    patient_name = serializers.CharField(source='patient.username', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'doctor_name', 'patient', 'patient_name', 'start_time', 'reason']

    def validate_start_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Cannot book appointment in the past.")
        return value

    def create(self, validated_data):
        # limit appointments per doctor per day (rate limit)
        doctor = validated_data['doctor']
        date = validated_data['start_time'].date()

        count = Appointment.objects.filter(doctor=doctor, start_time__date=date).count()
        if count >= 5:  # max 5 appointments per doctor per day
            raise serializers.ValidationError("Doctor has reached daily appointment limit.")
        return super().create(validated_data)


#💊 4.4 Prescription Serializer

class PrescriptionSerializer(serializers.ModelSerializer):
    appointment_detail = AppointmentSerializer(source='appointment', read_only=True)

    class Meta:
        model = Prescription
        fields = ['id', 'appointment', 'appointment_detail', 'notes', 'created_at']


#📄 4.5 File Upload Serializer
class FileUploadSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)

    class Meta:
        model = FileUpload
        fields = ['id', 'file', 'uploaded_by', 'uploaded_by_name', 'uploaded_at']
        read_only_fields = ['uploaded_by']
