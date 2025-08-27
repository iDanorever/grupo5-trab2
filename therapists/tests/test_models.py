from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Therapist
from datetime import date, time

class TherapistModelTest(TestCase):
    def setUp(self):
        self.therapist_data = {
            'document_type': 'DNI',
            'document_number': '12345678',
            'last_name_paternal': 'García',
            'last_name_maternal': 'López',
            'first_name': 'Juan',
            'birth_date': date(1990, 1, 1),
            'gender': 'Masculino',
            'phone': '123456789',
            'email': 'juan@example.com'
        }

    def test_create_therapist(self):
        therapist = Therapist.objects.create(**self.therapist_data)
        self.assertEqual(therapist.first_name, 'Juan')
        self.assertEqual(therapist.last_name_paternal, 'García')
        self.assertTrue(therapist.is_active)

    def test_therapist_str_representation(self):
        therapist = Therapist.objects.create(**self.therapist_data)
        expected = "Juan García López"
        self.assertEqual(str(therapist), expected)