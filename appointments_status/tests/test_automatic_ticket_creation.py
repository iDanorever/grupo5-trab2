from django.test import TestCase
from django.utils import timezone
from datetime import date, time
from decimal import Decimal
from ..models import Appointment, Ticket, AppointmentStatus
from ..services import AppointmentService, TicketService


class AutomaticTicketCreationTest(TestCase):
    """
    Pruebas para verificar la creación automática de tickets al crear citas.
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Crear estado de cita
        self.status = AppointmentStatus.objects.create(
            name="Pendiente",
            description="Cita pendiente",
            color="#FFA500"
        )
        
        # Crear datos de prueba para paciente y terapeuta (mocks)
        # En un entorno real, estos serían objetos reales de otros módulos
        self.patient_id = 1  # Mock ID
        self.therapist_id = 1  # Mock ID
    
    def test_create_appointment_creates_ticket_automatically(self):
        """Prueba que al crear una cita se crea automáticamente un ticket."""
        # Datos de la cita
        appointment_data = {
            'patient_id': self.patient_id,
            'therapist_id': self.therapist_id,
            'appointment_date': date(2024, 12, 25),
            'appointment_hour': time(10, 0),
            'payment': Decimal('150.00'),
            'appointment_status': self.status
        }
        
        # Crear la cita
        appointment = Appointment.objects.create(**appointment_data)
        
        # Verificar que se creó el ticket automáticamente
        self.assertTrue(Ticket.objects.filter(appointment=appointment).exists())
        
        # Obtener el ticket creado
        ticket = Ticket.objects.get(appointment=appointment)
        
        # Verificar que el ticket tiene los datos correctos
        self.assertEqual(ticket.amount, Decimal('150.00'))
        self.assertEqual(ticket.payment_method, 'efectivo')
        self.assertEqual(ticket.status, 'pending')
        self.assertTrue(ticket.ticket_number.startswith('TKT-'))
        
        # Verificar que el número de ticket se guardó en la cita
        self.assertEqual(appointment.ticket_number, ticket.ticket_number)
    
    def test_create_appointment_without_payment_creates_ticket_with_zero_amount(self):
        """Prueba que al crear una cita sin pago se crea un ticket con monto 0."""
        # Datos de la cita sin pago
        appointment_data = {
            'patient_id': self.patient_id,
            'therapist_id': self.therapist_id,
            'appointment_date': date(2024, 12, 26),
            'appointment_hour': time(11, 0),
            'appointment_status': self.status
        }
        
        # Crear la cita
        appointment = Appointment.objects.create(**appointment_data)
        
        # Verificar que se creó el ticket automáticamente
        ticket = Ticket.objects.get(appointment=appointment)
        self.assertEqual(ticket.amount, Decimal('0.00'))
    
    def test_update_appointment_payment_updates_ticket_amount(self):
        """Prueba que al actualizar el pago de una cita se actualiza el monto del ticket."""
        # Crear cita inicial
        appointment = Appointment.objects.create(
            patient_id=self.patient_id,
            therapist_id=self.therapist_id,
            appointment_date=date(2024, 12, 27),
            appointment_hour=time(14, 0),
            payment=Decimal('100.00'),
            appointment_status=self.status
        )
        
        # Verificar ticket inicial
        ticket = Ticket.objects.get(appointment=appointment)
        self.assertEqual(ticket.amount, Decimal('100.00'))
        
        # Actualizar el pago de la cita
        appointment.payment = Decimal('200.00')
        appointment.save()
        
        # Verificar que el ticket se actualizó
        ticket.refresh_from_db()
        self.assertEqual(ticket.amount, Decimal('200.00'))
    
    def test_delete_appointment_deactivates_ticket(self):
        """Prueba que al eliminar una cita se desactiva el ticket asociado."""
        # Crear cita
        appointment = Appointment.objects.create(
            patient_id=self.patient_id,
            therapist_id=self.therapist_id,
            appointment_date=date(2024, 12, 28),
            appointment_hour=time(15, 0),
            payment=Decimal('120.00'),
            appointment_status=self.status
        )
        
        # Verificar que el ticket está activo
        ticket = Ticket.objects.get(appointment=appointment)
        self.assertTrue(ticket.is_active)
        
        # Eliminar la cita (soft delete)
        appointment.is_active = False
        appointment.save()
        
        # Verificar que el ticket también se desactivó
        ticket.refresh_from_db()
        self.assertFalse(ticket.is_active)
    
    def test_ticket_number_uniqueness(self):
        """Prueba que los números de ticket son únicos."""
        # Crear múltiples citas
        appointments = []
        for i in range(5):
            appointment = Appointment.objects.create(
                patient_id=self.patient_id,
                therapist_id=self.therapist_id,
                appointment_date=date(2024, 12, 29 + i),
                appointment_hour=time(9 + i, 0),
                payment=Decimal('100.00'),
                appointment_status=self.status
            )
            appointments.append(appointment)
        
        # Obtener todos los tickets
        tickets = Ticket.objects.filter(appointment__in=appointments)
        
        # Verificar que todos tienen números únicos
        ticket_numbers = [ticket.ticket_number for ticket in tickets]
        self.assertEqual(len(ticket_numbers), len(set(ticket_numbers)))
    
    def test_service_create_appointment_with_ticket(self):
        """Prueba que el servicio de citas crea tickets automáticamente."""
        service = AppointmentService()
        
        # Datos de la cita
        appointment_data = {
            'patient_id': self.patient_id,
            'therapist_id': self.therapist_id,
            'appointment_date': date(2024, 12, 30),
            'appointment_hour': time(16, 0),
            'payment': Decimal('180.00'),
            'appointment_status': self.status
        }
        
        # Crear cita usando el servicio
        response = service.create(appointment_data)
        
        # Verificar que la respuesta es exitosa
        self.assertEqual(response.status_code, 201)
        
        # Verificar que se creó la cita y el ticket
        self.assertTrue(Appointment.objects.filter(
            appointment_date=date(2024, 12, 30),
            appointment_hour=time(16, 0)
        ).exists())
        
        appointment = Appointment.objects.get(
            appointment_date=date(2024, 12, 30),
            appointment_hour=time(16, 0)
        )
        
        self.assertTrue(Ticket.objects.filter(appointment=appointment).exists())
    
    def test_ticket_service_generate_unique_number(self):
        """Prueba que el servicio de tickets genera números únicos."""
        service = TicketService()
        
        # Generar múltiples números
        numbers = []
        for _ in range(10):
            number = service.generate_ticket_number()
            numbers.append(number)
        
        # Verificar que todos son únicos
        self.assertEqual(len(numbers), len(set(numbers)))
        
        # Verificar formato
        for number in numbers:
            self.assertTrue(number.startswith('TICKET-'))
            self.assertIn('-', number)
