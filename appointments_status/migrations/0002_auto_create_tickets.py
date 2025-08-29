# Generated manually for automatic ticket creation

from django.db import migrations
from django.utils import timezone
import uuid


def create_tickets_for_existing_appointments(apps, schema_editor):
    """
    Crea tickets para citas existentes que no tengan tickets asociados.
    """
    Appointment = apps.get_model('appointments_status', 'Appointment')
    Ticket = apps.get_model('appointments_status', 'Ticket')
    
    # Obtener citas que no tienen tickets
    appointments_without_tickets = Appointment.objects.filter(
        is_active=True
    ).exclude(
        id__in=Ticket.objects.values_list('appointment_id', flat=True)
    )
    
    # Contador para números secuenciales
    ticket_counter = 1
    
    for appointment in appointments_without_tickets:
        # Generar número de ticket único en formato secuencial
        ticket_number = f'TKT-{ticket_counter:03d}'
        ticket_counter += 1
        
        # Crear el ticket
        Ticket.objects.create(
            appointment=appointment,
            ticket_number=ticket_number,
            amount=appointment.payment or 0.00,
            payment_method='efectivo',
            description=f'Ticket generado automáticamente para cita #{appointment.id} (migración)',
            status='pending'
        )
        
        # Actualizar el número de ticket en la cita
        appointment.ticket_number = ticket_number
        appointment.save(update_fields=['ticket_number'])


def reverse_create_tickets_for_existing_appointments(apps, schema_editor):
    """
    Revierte la creación de tickets para citas existentes.
    """
    Ticket = apps.get_model('appointments_status', 'Ticket')
    # Eliminar tickets creados por esta migración
    Ticket.objects.filter(
        description__contains='(migración)'
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('appointments_status', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_tickets_for_existing_appointments,
            reverse_create_tickets_for_existing_appointments
        ),
    ]
