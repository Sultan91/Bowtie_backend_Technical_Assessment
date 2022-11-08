from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
#from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin

from .models import Doctor, Address, ConsultationFee, Schedule, Workday


class AddressSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = (
            'id',
            'address_1',
            'address_2',
            'address_3',
            'state',
            'city',
            'district',
            'postal_code',
            'country',
        )

    def get_country(self, obj):
        return obj.country.code


class ConsultationFeeSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = ConsultationFee

        fields = (
            'amount',
            'currency',
            'western_medicine_days'
        )

    def get_amount(self, obj):
        return float(obj.amount.amount)


class WorkdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Workday
        fields = (
            'id',
            'name',
            'time_from',
            'time_to'
        )


class ScheduleSerializer(serializers.ModelSerializer):
    days = serializers.SerializerMethodField()

    class Meta:
        model = Schedule

        fields = (
            'id',
            'works_on_holidays',
            'days'
        )

    def get_days(self, obj):
        return WorkdaySerializer(obj.workdays.all(), many=True).data


class DoctorSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            'id',
            'first_name',
            'last_name',
            'address',
            'service',
            'consultation_fee',
            'schedule',
            'language'
        )

    expandable_fields = dict(
        address=AddressSerializer,
        consultation_fee=ConsultationFeeSerializer,
        schedule=ScheduleSerializer
    )


