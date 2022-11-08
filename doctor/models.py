from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField, CurrencyField
from .choices import DOCTOR_SPECIFICATION_CHOICES, DAY_CHOICES, LANGUAGE_CHOICES
from .managers import DoctorManager
from django.conf import settings


# Create your models here.


class Address(models.Model):
    address_1 = models.CharField(blank=True, max_length=255)
    address_2 = models.CharField(blank=True, max_length=255)
    address_3 = models.CharField(blank=True, max_length=255)
    state = models.CharField(blank=True, max_length=64)
    city = models.CharField(blank=True, max_length=64)
    district = models.CharField(blank=True, max_length=64)
    postal_code = models.CharField(blank=True, max_length=16)
    country = CountryField(blank_label='(select country)', blank=True)

    def __str__(self):
        return f"{self.address_1} {self.district} {self.country.code}"


class ConsultationFee(models.Model):
    amount = MoneyField(max_digits=10, decimal_places=2)
    currency = CurrencyField(default=settings.DEFAULT_CURRENCY)
    western_medicine_days = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.amount} {self.currency}"


class Schedule(models.Model):
    works_on_holidays = models.BooleanField(default=False)


class Doctor(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    address = models.ForeignKey(Address, related_name='+', blank=True, default=None, null=True,
                                on_delete=models.DO_NOTHING)
    service = models.CharField(default=DOCTOR_SPECIFICATION_CHOICES.other, choices=DOCTOR_SPECIFICATION_CHOICES,
                                  blank=True, max_length=60)
    consultation_fee = models.OneToOneField(ConsultationFee, on_delete=models.SET_NULL, null=True, blank=True,
                                            related_name='doctor')
    schedule = models.OneToOneField(Schedule, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor')
    language = models.CharField(default=LANGUAGE_CHOICES.english, choices=LANGUAGE_CHOICES, blank=True, max_length=60)

    objects = DoctorManager()


class Workday(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='workdays')
    name = models.CharField(blank=True, max_length=256, choices=DAY_CHOICES)
    time_from = models.TimeField(blank=True)
    time_to = models.TimeField(blank=True)



