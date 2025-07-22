from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Prescription

@receiver(post_save, sender=Prescription)
def send_prescription_notification(sender, instance, created, **kwargs):
    if created:
        patient = instance.appointment.patient
        doctor = instance.appointment.doctor
        subject = f"🩺 New Prescription from Dr. {doctor.username}"
        message = f"Hello {patient.username},\n\nYou have received a new prescription:\n\n{instance.notes}\n\nThanks,\nHealthCare App"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [patient.email]

        try:
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)
            print("✅ Email sent to patient.")
        except Exception as e:
            print("❌ Email failed:", e)
