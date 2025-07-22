from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

from django.contrib.auth import get_user_model

from .models import Appointment, Prescription, FileUpload
from .serializers import (
    UserSerializer,
    AppointmentSerializer,
    PrescriptionSerializer,
    FileUploadSerializer,
)
from .permissions import IsDoctor, IsPatient, IsOwnerOrReadOnly
from datetime import timedelta
from django.utils import timezone
from .tasks import send_appointment_reminder
from celery import current_app

User = get_user_model()

#Create a Custom JWT View
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


#📝 5.3 Signup View

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

#📅 5.4 Appointment Views

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related('doctor', 'patient').all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Roles.DOCTOR:
            return self.queryset.filter(doctor=user)
        elif user.role == User.Roles.PATIENT:
            return self.queryset.filter(patient=user)
        return self.queryset.none()

    def perform_create(self, serializer):
        user = self.request.user
        appointment = serializer.save(patient=user if user.role == "PATIENT" else None)

        # Schedule Celery task: 1 hour before appointment time
        reminder_time = appointment.start_time - timedelta(hours=1)
        delay = (reminder_time - timezone.now()).total_seconds()

        if delay > 0:
            send_appointment_reminder.apply_async((appointment.id,), countdown=delay)

#💊 5.5 Prescription View

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.select_related('appointment__doctor', 'appointment__patient').all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsDoctor]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Roles.DOCTOR:
            return self.queryset.filter(appointment__doctor=user)
        return self.queryset.none()


#📄 5.6 File Upload View

class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.select_related('uploaded_by').all()
    serializer_class = FileUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(uploaded_by=user)




class TestEmailView(APIView):
    def get(self, request):
        send_mail(
            'Hello from Django!',
            'This is a test email using Gmail SMTP.',
            'yogalakshmi3000@gmail.com',
            ['squadpi4723@gmail.com'],
            fail_silently=False,
        )
        return Response({'message': 'Email sent successfully!'})