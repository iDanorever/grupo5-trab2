# Creación Automática de Tickets

## Descripción

Este módulo implementa la funcionalidad de **creación automática de tickets** cuando se crea una cita médica. Cada vez que se crea una nueva cita, el sistema automáticamente genera un ticket asociado con un número único.

## Funcionalidades Implementadas

### 1. Signals de Django

**Archivo:** `appointments_status/signals.py`

- **`create_ticket_for_appointment`**: Se ejecuta automáticamente después de crear una cita
- **`update_ticket_when_appointment_changes`**: Sincroniza cambios en la cita con el ticket
- **`generate_unique_ticket_number`**: Genera números únicos de ticket

### 2. Servicios Implementados

**Archivo:** `appointments_status/services/appointment_service.py`

- Creación de citas con validación de datos
- Verificación automática de creación de tickets
- Manejo de errores y transacciones
- Filtros y paginación
- Verificación de disponibilidad

**Archivo:** `appointments_status/services/ticket_service.py`

- Gestión completa de tickets
- Generación de números únicos
- Cambios de estado (pagado, cancelado)
- Filtros y estadísticas

### 3. Vistas Actualizadas

**Archivo:** `appointments_status/views/appointment.py`

- Integración con servicios
- Endpoints adicionales para verificación de disponibilidad
- Cancelación y reprogramación de citas

**Archivo:** `appointments_status/views/ticket.py`

- Gestión completa de tickets
- Estadísticas y reportes
- Filtros avanzados

## Flujo de Creación Automática

1. **Usuario crea una cita** → POST `/api/appointments/`
2. **Signal se ejecuta** → `create_ticket_for_appointment`
3. **Se genera número único** → `TICKET-YYYYMMDDHHMMSS-XXXXXXXX`
4. **Se crea el ticket** → Con datos de la cita
5. **Se actualiza la cita** → Con el número de ticket
6. **Respuesta exitosa** → Cita + Ticket creados

## Configuración de Signals

Los signals se registran automáticamente en:

```python
# appointments_status/apps.py
def ready(self):
    import appointments_status.signals
```

## Estructura del Número de Ticket

Formato: `TKT-XXX` (secuencial)

- **TKT**: Prefijo fijo
- **XXX**: Número secuencial con ceros a la izquierda

Ejemplos: `TKT-001`, `TKT-002`, `TKT-010`, `TKT-100`

## Datos Automáticos del Ticket

Cuando se crea automáticamente, el ticket incluye:

- **Número único**: Generado automáticamente
- **Monto**: Del campo `payment` de la cita (o 0.00 si no hay)
- **Método de pago**: "efectivo" por defecto
- **Estado**: "pending" por defecto
- **Descripción**: "Ticket generado automáticamente para cita #X"

## Endpoints Disponibles

### Citas
- `POST /api/appointments/` - Crear cita (con ticket automático)
- `GET /api/appointments/` - Listar citas
- `GET /api/appointments/{id}/` - Obtener cita específica
- `PUT /api/appointments/{id}/` - Actualizar cita
- `DELETE /api/appointments/{id}/` - Eliminar cita
- `GET /api/appointments/completed/` - Citas completadas
- `GET /api/appointments/pending/` - Citas pendientes
- `GET /api/appointments/by_date_range/` - Citas por rango de fechas
- `GET /api/appointments/check_availability/` - Verificar disponibilidad
- `POST /api/appointments/{id}/cancel/` - Cancelar cita
- `POST /api/appointments/{id}/reschedule/` - Reprogramar cita

### Tickets
- `GET /api/tickets/` - Listar tickets
- `GET /api/tickets/{id}/` - Obtener ticket específico
- `PUT /api/tickets/{id}/` - Actualizar ticket
- `DELETE /api/tickets/{id}/` - Eliminar ticket
- `GET /api/tickets/paid/` - Tickets pagados
- `GET /api/tickets/pending/` - Tickets pendientes
- `GET /api/tickets/cancelled/` - Tickets cancelados
- `POST /api/tickets/{id}/mark_as_paid/` - Marcar como pagado
- `POST /api/tickets/{id}/mark_as_cancelled/` - Marcar como cancelado
- `GET /api/tickets/statistics/` - Estadísticas de tickets

## Ejemplo de Uso

### Crear una Cita (con ticket automático)

```bash
POST /api/appointments/
Content-Type: application/json

{
    "patient": 1,
    "therapist": 1,
    "appointment_date": "2024-12-25",
    "appointment_hour": "10:00:00",
    "payment": 150.00,
    "appointment_type": "Consulta general"
}
```

**Respuesta:**
```json
{
    "message": "Cita creada exitosamente con ticket automático",
    "appointment": {
        "id": 1,
        "patient": 1,
        "therapist": 1,
        "appointment_date": "2024-12-25",
        "appointment_hour": "10:00:00",
        "payment": "150.00",
        "ticket_number": "TKT-001",
        ...
    },
    "ticket_number": "TKT-001"
}
```

## Pruebas

Las pruebas están en `appointments_status/tests/test_automatic_ticket_creation.py`:

- Creación automática de tickets
- Unicidad de números de ticket
- Sincronización de cambios
- Eliminación en cascada
- Funcionalidad de servicios

## Consideraciones Técnicas

### Transacciones
- Todas las operaciones usan `@transaction.atomic`
- Rollback automático en caso de error

### Validaciones
- Campos requeridos verificados
- Formato de fechas y horas validado
- Unicidad de números de ticket

### Performance
- Signals optimizados para evitar loops infinitos
- Consultas eficientes con filtros
- Paginación implementada

## Dependencias

- Django 3.2+
- Django REST Framework
- UUID para generación de números únicos
- Transacciones de base de datos

## Estado del Requerimiento

✅ **CUMPLIDO**: La funcionalidad de creación automática de tickets al crear citas está completamente implementada y funcional.

### ✅ Cambios Recientes - Formato Secuencial

**Antes:** `TICKET-YYYYMMDDHHMMSS-XXXXXXXX`
**Ahora:** `TKT-001`, `TKT-002`, `TKT-003`, etc.

- ✅ Formato secuencial implementado
- ✅ Números con ceros a la izquierda (001, 002, 010, 100)
- ✅ Compatibilidad con tickets existentes
- ✅ Pruebas actualizadas
- ✅ Documentación actualizada
