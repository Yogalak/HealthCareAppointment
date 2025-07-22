from django.contrib import admin

# Register your models here.
#🧑‍💻 3.3 Configure admin.py (core/admin.py)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Appointment, Prescription, FileUpload

# Custom User admin with role field
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    list_display = ['username', 'email', 'role', 'is_staff']

# Appointment admin
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'start_time', 'reason')
    list_filter = ('start_time', 'doctor', 'patient')
    search_fields = ('doctor__username', 'patient__username')

# Prescription admin
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'created_at')
    search_fields = ('appointment__doctor__username', 'appointment__patient__username')

# File Upload admin
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('uploaded_by', 'file', 'uploaded_at')
    search_fields = ('uploaded_by__username',)

# Registering models
admin.site.register(User, UserAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(FileUpload, FileUploadAdmin)
