from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Appointment, Ticket
import re


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
    Genera un número de ticket único en formato secuencial TKT-001, TKT-002, etc.
    """
    from .models import Ticket
    
    # Obtener el último ticket creado
    last_ticket = Ticket.objects.order_by('-id').first()
    
    if last_ticket:
        # Extraer el número del último ticket
        try:
            # Buscar el patrón TKT-XXX en el número del ticket
            match = re.search(r'TKT-(\d+)', last_ticket.ticket_number)
            if match:
                last_number = int(match.group(1))
                next_number = last_number + 1
            else:
                # Si no encuentra el patrón, empezar desde 1
                next_number = 1
        except (ValueError, AttributeError):
            # Si hay algún error, empezar desde 1
            next_number = 1
    else:
        # Si no hay tickets, empezar desde 1
        next_number = 1
    
    # Formatear el número con ceros a la izquierda (ej: 001, 002, 010, 100)
    return f'TKT-{next_number:03d}'


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
