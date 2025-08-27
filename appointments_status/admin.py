from django.contrib import admin
from .models import Appointment, AppointmentStatus, Ticket


@admin.register(AppointmentStatus)
class AppointmentStatusAdmin(admin.ModelAdmin):
    """
    Configuración del admin para AppointmentStatus.
    """
    list_display = ['name', 'description', 'appointments_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    readonly_fields = ['appointments_count', 'created_at', 'updated_at']
    ordering = ['name']

    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Información del Sistema', {
            'fields': ('appointments_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# --- Inline opcional para crear/ver Tickets desde la Cita ---
class TicketInline(admin.StackedInline):
    model = Ticket
    extra = 0
    autocomplete_fields = ['appointment']  # no carga listas enormes
    readonly_fields = ['is_paid', 'is_pending', 'payment_date', 'created_at', 'updated_at']
    fieldsets = (
        ('Información del Ticket', {
            'fields': ('ticket_number', 'amount', 'payment_method', 'description')
        }),
        ('Estado del Pago', {
            'fields': ('status',)
        }),
        ('Relaciones', {
            'fields': ('appointment',),
            'description': 'La cita se completa automáticamente al usar el inline.'
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Información del Sistema', {
            'fields': ('is_paid', 'is_pending', 'payment_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'appointment_date', 'appointment_hour', 'appointment_type',
        'room', 'appointment_status', 'is_completed', 'is_active'
    ]
    list_filter = [
        'appointment_date', 'appointment_status', 'appointment_type',
        'room', 'is_active', 'created_at'
    ]
    search_fields = ['ailments', 'diagnosis', 'observation', 'ticket_number']
    readonly_fields = ['is_completed', 'is_pending', 'created_at', 'updated_at']
    ordering = ['-appointment_date', '-appointment_hour']

    # 👇 según prefieras
    raw_id_fields = ['patient', 'therapist']
    # o bien
    # autocomplete_fields = ['patient', 'therapist']

    fieldsets = (
        ('Información de la Cita', {
            'fields': ('appointment_date', 'appointment_hour', 'appointment_type', 'room')
        }),
        ('Información Médica', {
            'fields': ('ailments', 'diagnosis', 'surgeries', 'reflexology_diagnostics', 'medications', 'observation')
        }),
        ('Fechas de Tratamiento', {
            'fields': ('initial_date', 'final_date')
        }),
        ('Información de Pago', {
            'fields': ('social_benefit', 'payment_detail', 'payment', 'ticket_number')
        }),
        ('Relaciones', {
            # 👇 ahora ambos son obligatorios
            'fields': ('patient', 'therapist', 'appointment_status'),
            'description': 'Selecciona paciente y terapeuta (ambos son obligatorios).'
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Información del Sistema', {
            'fields': ('is_completed', 'is_pending', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return (super()
                .get_queryset(request)
                .select_related('appointment_status', 'patient', 'therapist'))


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Ticket.
    """
    list_display = [
        'ticket_number', 'amount', 'payment_method', 'status',
        'is_paid', 'payment_date', 'is_active'
    ]
    list_filter = [
        'payment_method', 'status', 'payment_date', 'is_active', 'created_at'
    ]
    search_fields = ['ticket_number', 'description']
    readonly_fields = ['is_paid', 'is_pending', 'payment_date', 'created_at', 'updated_at']
    ordering = ['-payment_date']

    # ✅ Para no cargar todas las citas en un <select>
    autocomplete_fields = ['appointment']  # (usa raw_id_fields = ['appointment'] si prefieres)

    fieldsets = (
        ('Información del Ticket', {
            'fields': ('ticket_number', 'amount', 'payment_method', 'description')
        }),
        ('Estado del Pago', {
            'fields': ('status',)
        }),
        ('Relaciones', {
            # ✅ Campo necesario para evitar el NOT NULL
            'fields': ('appointment',),
            'description': 'Selecciona la cita a la que pertenece este ticket'
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Información del Sistema', {
            'fields': ('is_paid', 'is_pending', 'payment_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_paid', 'mark_as_cancelled']

    def mark_as_paid(self, request, queryset):
        """Acción para marcar tickets como pagados"""
        updated = queryset.update(status='paid')
        self.message_user(request, f'{updated} tickets marcados como pagados.')
    mark_as_paid.short_description = "Marcar como pagado"

    def mark_as_cancelled(self, request, queryset):
        """Acción para marcar tickets como cancelados"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} tickets marcados como cancelados.')
    mark_as_cancelled.short_description = "Marcar como cancelado"

    def get_queryset(self, request):
        """Optimiza las consultas con select_related"""
        return super().get_queryset(request).select_related('appointment')

    def get_changeform_initial_data(self, request):
        """
        Permite precargar la cita si vienes con ?appointment=<id> en la URL de alta:
        /admin/appointments_status/ticket/add/?appointment=123
        """
        initial = super().get_changeform_initial_data(request)
        aid = request.GET.get("appointment")
        if aid:
            initial["appointment"] = aid
        return initial
