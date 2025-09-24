import requests # type: ignore
from datetime import timedelta
from django.conf import settings

GHL_API_URL = "https://services.leadconnectorhq.com/calendars/events/appointments"

def crear_cita_en_ghl(cita, contact_id):
    headers = {
        "Authorization": f"Bearer {settings.GHL_API_KEY}",
        "Content-Type": "application/json",
        "Version": "2021-04-15"
    }

    payload = {
        "title": f"Cita con {cita.paciente}",
        "calendarId": settings.GHL_CALENDAR_ID,
        "locationId": settings.GHL_LOCATION_ID,
        "contactId": contact_id,
        "appointmentStatus": "confirmed",
        "meetingLocationType": "custom",
        "overrideLocationConfig": True,
        "startTime": cita.fecha.isoformat(),
        "endTime": (cita.fecha + timedelta(minutes=cita.duracion)).isoformat(),
        "description": "Cita creada desde ReflexoPeru v3",
    }

    response = requests.post(GHL_API_URL, json=payload, headers=headers)
    response.raise_for_status()  # Lanza error si la respuesta no es 200
    return response.json()