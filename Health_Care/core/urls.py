from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    AppointmentViewSet,
    PrescriptionViewSet,
    FileUploadViewSet,
)
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#)
from .views import TestEmailView
from .views import CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointments')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescriptions')
router.register(r'uploads', FileUploadViewSet, basename='uploads')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),     # login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
     path('test-email/', TestEmailView.as_view()),
]
