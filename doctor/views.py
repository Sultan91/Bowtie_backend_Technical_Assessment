from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from .filters import DoctorFilter
from .models import Doctor
from .serializers import DoctorSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = DoctorFilter
    search_fields = (
        'first_name',
        'last_name'
    )
    ordering_fields = (
        ('first_name', 'last_name'),
    )







