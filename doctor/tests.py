from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .choices import DOCTOR_SPECIFICATION_CHOICES, DAY_CHOICES
from .models import Doctor, Address, ConsultationFee, Schedule, Workday
import datetime


# Create your tests here.


class DoctorListViewTests(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('doctor:doctors-list')
        self.address = Address.objects.create(
            address_1='test street',
            city='HK',
            district='Center',
            country='CN'
        )
        self.fee = ConsultationFee.objects.create(
            amount=90,
            currency='USD',
            western_medicine_days=3
        )
        self.schedule1 = Schedule.objects.create()
        self.workday_1 = Workday.objects.create(
            name=DAY_CHOICES.monday,
            time_from=datetime.time(9, 0, 0),
            time_to=datetime.time(12, 0, 0),
            schedule=self.schedule1
        )
        self.workday_2 = Workday.objects.create(
            name=DAY_CHOICES.wednesday,
            time_from=datetime.time(15, 0, 0),
            time_to=datetime.time(18, 0, 0),
            schedule=self.schedule1
        )
        self.schedule2 = Schedule.objects.create()
        self.workday_3 = Workday.objects.create(
            name=DAY_CHOICES.tuesday,
            time_from=datetime.time(8, 0, 0),
            time_to=datetime.time(12, 0, 0),
            schedule=self.schedule2
        )
        self.workday_4 = Workday.objects.create(
            name=DAY_CHOICES.wednesday,
            time_from=datetime.time(11, 0, 0),
            time_to=datetime.time(18, 0, 0),
            schedule=self.schedule2
        )

    def test_create_doctor(self):
        data = {
            'first_name': 'Test',
            'last_name': 'Test',
            'address': self.address.id,
            'service': DOCTOR_SPECIFICATION_CHOICES.general_practitioner,
            'consultation_fee': self.fee.id,
            'schedule': self.schedule1.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        doctor = Doctor.objects.last()
        self.assertEqual(data['first_name'], doctor.first_name)
        self.assertEqual(data['last_name'], doctor.last_name)
        self.assertEqual(data['service'], doctor.service)
        self.assertEqual(data['address'], doctor.address_id)
        self.assertEqual(data['consultation_fee'], doctor.consultation_fee_id)
        self.assertEqual(data['schedule'], doctor.schedule_id)

    def test_get_doctor_detail(self):
        doctor1 = Doctor.objects.create(first_name='test doc detailed', schedule=self.schedule1,
                                        consultation_fee=self.fee)
        url = reverse('doctor:doctors-detail', args=(doctor1.id,))
        response = self.client.get(url)
        self.assertEqual(response.json(),
                         {'id': doctor1.id, 'first_name': doctor1.first_name, 'last_name': doctor1.last_name,
                          'address': doctor1.address, 'service': doctor1.service, 'consultation_fee':
                              doctor1.consultation_fee_id, 'schedule': doctor1.schedule_id,
                          'language': doctor1.language,
                          }
                         )

    def test_list_doctors(self):
        fee1 = ConsultationFee.objects.create(
            amount=30,
            currency='USD',
            western_medicine_days=1
        )
        doctor1 = Doctor.objects.create(first_name='test doc 1', schedule=self.schedule1, consultation_fee=self.fee)
        doctor2 = Doctor.objects.create(first_name='test doc 2', schedule=self.schedule2, consultation_fee=fee1,
                                        service=DOCTOR_SPECIFICATION_CHOICES.pediatrician)
        response = self.client.get(self.url)
        self.assertEqual(response.json(),
                         [{'id': doctor1.id, 'first_name': doctor1.first_name, 'last_name': doctor1.last_name,
                           'address': doctor1.address, 'service': doctor1.service, 'language': doctor1.language,
                           'consultation_fee': doctor1.consultation_fee_id, 'schedule': doctor1.schedule_id},
                          {'id': doctor2.id, 'first_name': doctor2.first_name, 'last_name': doctor2.last_name,
                           'address': doctor2.address, 'service': doctor2.service, 'language': doctor1.language,
                           'consultation_fee': doctor2.consultation_fee_id, 'schedule': doctor2.schedule_id}
                          ]
                         )

    def test_list_doctors_expand_fee(self):
        fee1 = ConsultationFee.objects.create(
            amount=30,
            currency='USD',
            western_medicine_days=1
        )
        doctor1 = Doctor.objects.create(first_name='test doc 1', address=self.address,
                                        schedule=self.schedule1, consultation_fee=fee1)
        response = self.client.get(self.url + "?expand=consultation_fee")
        self.assertEqual(response.json(),
                         [{'id': doctor1.id, 'first_name': doctor1.first_name, 'last_name': doctor1.last_name,
                           'address': doctor1.address_id, 'service': doctor1.service,
                           'language': doctor1.language,
                           'consultation_fee': {'amount': float(fee1.amount.amount), 'currency': fee1.currency,
                                                'western_medicine_days': fee1.western_medicine_days},
                           'schedule': 1}]
                         )

    def test_list_doctors_expand_schedule(self):
        doctor1 = Doctor.objects.create(first_name='test doc 1', address=self.address,
                                        schedule=self.schedule1, consultation_fee=self.fee)
        response = self.client.get(self.url + "?expand=schedule")
        self.assertEqual(response.json(),
                         [{'id': doctor1.id, 'first_name': doctor1.first_name, 'last_name': doctor1.last_name,
                           'address': doctor1.address_id,
                           'service': doctor1.service, 'consultation_fee': doctor1.consultation_fee_id,
                           'language': doctor1.language,
                           'schedule': {'id': doctor1.schedule_id,
                                        'works_on_holidays': self.schedule1.works_on_holidays,
                                        'days':
                                            [{'name': self.workday_1.name,
                                              'time_from': self.workday_1.time_from.strftime("%H:%M:%S"),
                                              'time_to': self.workday_1.time_to.strftime("%H:%M:%S"),
                                              'id': self.workday_1.id},
                                             {'name': self.workday_2.name,
                                              'time_from': self.workday_2.time_from.strftime("%H:%M:%S"),
                                              'time_to': self.workday_2.time_to.strftime("%H:%M:%S"),
                                              'id': self.workday_2.id}]}}]

                         )

    def test_list_doctors_expand_address(self):
        doctor1 = Doctor.objects.create(first_name='test doc 3', address=self.address,
                                        schedule=self.schedule1, consultation_fee=self.fee)
        response = self.client.get(self.url + "?expand=address")
        self.assertEqual(response.json(),
                         [{
                             'id': doctor1.id, 'first_name': doctor1.first_name, 'last_name': doctor1.last_name,
                             'address': {'id': self.address.id, 'address_1': self.address.address_1,
                                         'address_2': self.address.address_2,
                                         'address_3': self.address.address_3, 'state': self.address.state,
                                         'city': self.address.city,
                                         'district': self.address.district,
                                         'postal_code': self.address.postal_code,
                                         'country': self.address.country},
                             'service': doctor1.service, 'consultation_fee': doctor1.consultation_fee_id,
                             'schedule': doctor1.schedule_id,
                             'language': doctor1.language,
                         }]
                         )

    def test_filter_by_district(self):
        address2 = Address.objects.create(
            address_1='test street',
            city='HK',
            district='Suburb',
            country='CN'
        )
        doctor1 = Doctor.objects.create(first_name='test doc 4', address=self.address)
        doctor2 = Doctor.objects.create(first_name='test doc 5', address=address2)
        url = self.url + "?district=Suburb&expand=address"
        response = self.client.get(url)
        self.assertEqual(response.json(),
                         [{
                             'id': doctor2.id, 'first_name': doctor2.first_name, 'last_name': doctor2.last_name,
                             'address': {'id': doctor2.address.id, 'address_1': doctor2.address.address_1,
                                         'address_2': doctor2.address.address_2, 'address_3': doctor2.address.address_3,
                                         'state': doctor2.address.state, 'city': doctor2.address.city,
                                         'district': doctor2.address.district,
                                         'postal_code': doctor2.address.postal_code,
                                         'country': doctor2.address.country.code},
                             'service': doctor2.service, 'consultation_fee': doctor2.consultation_fee,
                             'schedule': doctor2.schedule,
                             'language': doctor2.language
                         }]
                         )

    def test_filter_by_category(self):
        doctor1 = Doctor.objects.create(first_name='test doc 4',
                                        service=DOCTOR_SPECIFICATION_CHOICES.general_practitioner)
        doctor2 = Doctor.objects.create(first_name='test doc 5', service=DOCTOR_SPECIFICATION_CHOICES.cardiologist)
        url = self.url + "?service=cardiologist"
        response = self.client.get(url)
        self.assertEqual(response.json(),
                         [{
                             'id': doctor2.id, 'first_name': doctor2.first_name, 'last_name': doctor2.last_name,
                             'address': doctor2.address,
                             'service': doctor2.service, 'consultation_fee': doctor2.consultation_fee,
                             'schedule': doctor2.schedule,
                             'language': doctor2.language
                         }]
                         )

    def test_filter_by_language(self):
        doctor1 = Doctor.objects.create(first_name='test doc 4', language='English')
        doctor2 = Doctor.objects.create(first_name='test doc 5', language='Chinese')
        url = self.url + "?language=Chinese"
        response = self.client.get(url)
        self.assertEqual(response.json(),
                         [{
                             'id': doctor2.id, 'first_name': doctor2.first_name, 'last_name': doctor2.last_name,
                             'address': doctor2.address, 'service': doctor2.service,
                             'consultation_fee': doctor2.consultation_fee, 'schedule': doctor2.schedule,
                             'language': doctor2.language
                         }]
                         )

    def test_filter_by_price(self):
        fee1 = ConsultationFee.objects.create(
            amount=10,
            currency='USD',
            western_medicine_days=1
        )
        fee2 = ConsultationFee.objects.create(
            amount=20,
            currency='USD',
            western_medicine_days=1
        )
        fee3 = ConsultationFee.objects.create(
            amount=40,
            currency='USD',
            western_medicine_days=1
        )
        doctor1 = Doctor.objects.create(consultation_fee=fee1)
        doctor2 = Doctor.objects.create(consultation_fee=fee2)
        doctor3 = Doctor.objects.create(consultation_fee=fee3)
        url = self.url + "?consultation_fee_lte=25&consultation_fee_gte=15"
        response = self.client.get(url)
        self.assertEqual(response.json(),
                         [{
                             'id': doctor2.id, 'first_name': doctor2.first_name, 'last_name': doctor2.last_name,
                             'address': doctor2.address, 'service': doctor2.service,
                             'consultation_fee': doctor2.consultation_fee_id, 'schedule': doctor2.schedule,
                             'language': doctor2.language
                         }]
                         )
