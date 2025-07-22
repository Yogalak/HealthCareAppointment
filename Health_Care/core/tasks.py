from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Appointment

@shared_task
def send_appointment_reminder(appointment_id):
    try:
        appointment = Appointment.objects.select_related('patient', 'doctor').get(id=appointment_id)
        if appointment.start_time > timezone.now():
            subject = f"Reminder: Appointment with Dr. {appointment.doctor.username}"
            message = f"Hello {appointment.patient.username},\n\nThis is a reminder for your appointment at {appointment.start_time}.\n\nReason: {appointment.reason}"
            recipient = [appointment.patient.email]
            send_mail(subject, message, None, recipient)
            print("✅ Reminder sent to patient")
    except Appointment.DoesNotExist:
        print("❌ Appointment not found")
