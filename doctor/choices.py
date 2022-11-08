from model_utils import Choices

DOCTOR_SPECIFICATION_CHOICES = Choices(
    ('general_practitioner', 'General Practitioner'),
    ('pediatrician', 'Pediatrician'),
    ('cardiologist', 'Cardiologist'),
    ('oncologist', 'Oncologist'),
    ('gastroenterologist', 'Gastroenterologist'),
    ('other', 'Other'),
)


DAY_CHOICES = Choices(
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
    ('saturday', 'Saturday'),
    ('sunday', 'Sunday'),
)


LANGUAGE_CHOICES = Choices(
    ('english', 'English'),
    ('mandarin', 'Mandarin'),
    ('kazakh', 'Kazakh'),
    ('other', 'Other'),
)