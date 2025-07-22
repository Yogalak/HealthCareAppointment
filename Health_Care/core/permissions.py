from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()

# ✅ Allow only DOCTOR users
class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == User.Roles.DOCTOR

# ✅ Allow only PATIENT users
class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == User.Roles.PATIENT

# ✅ Allow only object owners to read/update
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.uploaded_by == request.user or request.method in permissions.SAFE_METHODS
