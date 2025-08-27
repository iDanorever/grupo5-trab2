from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Therapist
from datetime import date, time

class TherapistViewsTest(APITestCase):
    def setUp(self):
        self.therapist_data = {
            'document_type': 'DNI',
            'document_number': '12345678',
            'last_name_paternal': 'García',
            'last_name_maternal': 'López',
            'first_name': 'Juan',
            'birth_date': '1990-01-01',
            'gender': 'M',  # Cambiado de 'Masculino' a 'M'
            'phone': '123456789',
            'email': 'juan@gmail.com'  # Cambiado para terminar en @gmail.com
        }
        self.therapist = Therapist.objects.create(**{
            'document_type': 'DNI',
            'document_number': '87654321',
            'last_name_paternal': 'García',
            'last_name_maternal': 'López',
            'first_name': 'Juan',
            'birth_date': date(1990, 1, 1),
            'gender': 'M',  # Cambiado de 'Masculino' a 'M'
            'phone': '123456789',
            'email': 'juan@gmail.com'  # Cambiado para terminar en @gmail.com
        })

    def test_create_therapist(self):
        url = reverse('therapist-list')
        response = self.client.post(url, self.therapist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Therapist.objects.count(), 2)

    def test_list_therapists(self):
        url = reverse('therapist-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_therapist(self):
        url = reverse('therapist-detail', args=[self.therapist.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Juan')

    def test_soft_delete_therapist(self):
        url = reverse('therapist-detail', args=[self.therapist.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.therapist.refresh_from_db()
        self.assertFalse(self.therapist.is_active)

    def test_restore_therapist(self):
        self.therapist.is_active = False
        self.therapist.save()
        url = reverse('therapist-restore', args=[self.therapist.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.therapist.refresh_from_db()
        self.assertTrue(self.therapist.is_active)