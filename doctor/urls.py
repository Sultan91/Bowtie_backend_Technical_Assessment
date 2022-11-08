
from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import DoctorViewSet

app_name = 'doctor'
router = DefaultRouter()
router.register('doctors', DoctorViewSet, basename='doctors')

urlpatterns = router.urls