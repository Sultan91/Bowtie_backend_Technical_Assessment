from django_filters import CharFilter, NumberFilter
from django_filters.rest_framework import FilterSet

from doctor.models import Doctor


class DoctorFilter(FilterSet):
    service = CharFilter(field_name="service", label="Service", lookup_expr="iexact", help_text='Search by service')
    language = CharFilter(field_name="language", label="Language", lookup_expr="iexact", help_text='Search by language')
    consultation_fee_lte = NumberFilter(label='Quantity less', method='filter_fee_lte')
    consultation_fee_gte = NumberFilter(label='Quantity greater', method='filter_fee_gte')
    district = CharFilter(label="City district", method='filter_by_district')

    def filter_fee_lte(self, qs, name, value):
        return qs.filter(consultation_fee__amount__lte=value)

    def filter_fee_gte(self, qs, name, value):
        return qs.filter(consultation_fee__amount__gte=value)

    def filter_by_district(self, qs, name, value):
        return qs.filter(address__district__iexact=value)

    class Meta:
        model = Doctor
        fields = ('service', 'language', 'district', 'consultation_fee_lte', 'consultation_fee_gte')

