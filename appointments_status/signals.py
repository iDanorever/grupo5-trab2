from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Appointment, Ticket
import uuid


@receiver(post_save, sender=Appointment)
def create_ticket_for_appointment(sender, instance, created, **kwargs):
    """
    Signal que se ejecuta después de crear una cita para crear automáticamente un ticket.
    """
    if created:
        # Generar número de ticket único
        ticket_number = generate_unique_ticket_number()
        
        # Crear el ticket automáticamente
        Ticket.objects.create(
            appointment=instance,
            ticket_number=ticket_number,
            amount=instance.payment or 0.00,  # Usar el pago de la cita o 0 por defecto
            payment_method='efectivo',  # Método por defecto
            description=f'Ticket generado automáticamente para cita #{instance.id}',
            status='pending'
        )
        
        # Actualizar el número de ticket en la cita
        instance.ticket_number = ticket_number
        instance.save(update_fields=['ticket_number'])


def generate_unique_ticket_number():
    """
    Genera un número de ticket único basado en timestamp.
    """
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return int(timestamp)


@receiver(post_save, sender=Appointment)
def update_ticket_when_appointment_changes(sender, instance, created, **kwargs):
    """
    Signal que se ejecuta cuando se actualiza una cita para sincronizar con el ticket.
    """
    if not created and instance.ticket_number:
        try:
            ticket = Ticket.objects.get(appointment=instance)
            # Actualizar el monto del ticket si cambió el pago de la cita
            if instance.payment and ticket.amount != instance.payment:
                ticket.amount = instance.payment
                ticket.save(update_fields=['amount', 'updated_at'])
        except Ticket.DoesNotExist:
            # Si no existe el ticket, crearlo
            create_ticket_for_appointment(sender, instance, False, **kwargs)
