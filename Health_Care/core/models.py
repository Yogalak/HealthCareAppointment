# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Custom User with roles
class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        DOCTOR = "DOCTOR", _("Doctor")
        PATIENT = "PATIENT", _("Patient")

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.PATIENT,
    )

    def is_doctor(self):
        return self.role == self.Roles.DOCTOR

    def is_patient(self):
        return self.role == self.Roles.PATIENT

    def is_admin(self):
        return self.role == self.Roles.ADMIN

#🩺 2.2 Appointment Model

class Appointment(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments_as_doctor')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments_as_patient')
    start_time = models.DateTimeField()
    reason = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_time']
        unique_together = ['doctor', 'start_time']  # prevent double-booking

    def __str__(self):
        return f"{self.patient.username} with Dr. {self.doctor.username} at {self.start_time}"


#💊 2.3 Prescription Model
class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='prescription')
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.appointment.patient.username}"

#📄 2.4 File Upload Model (Lab Reports or PDFs)

def report_upload_path(instance, filename):
    return f"reports/user_{instance.uploaded_by.id}/{filename}"

class FileUpload(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to=report_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File by {self.uploaded_by.username}"

