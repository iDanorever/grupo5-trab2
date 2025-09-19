import requests
import os
from decouple import config

class GHLService:
    # 🔑 Guarda tu API key en el archivo .env
    BASE_URL = "https://rest.gohighlevel.com/v1"
    API_KEY = config("GHL_API_KEY", default=os.getenv("GHL_API_KEY"))
    DEFAULT_LOCATION_ID = config("GHL_LOCATION_ID", default=os.getenv("GHL_LOCATION_ID"))
    DEFAULT_CALENDAR_ID = config("GHL_CALENDAR_ID", default=os.getenv("GHL_CALENDAR_ID"))

    @classmethod
    def create_appointment(cls, appointment_data, calendar_id=None):
        if not cls.API_KEY:
            raise RuntimeError("GHL_API_KEY no configurado en variables de entorno")

        url = f"{cls.BASE_URL}/calendars/events/appointments"
        headers = {
            "Authorization": f"Bearer {cls.API_KEY}",
            "Content-Type": "application/json"
        }

        resolved_calendar_id = calendar_id or cls.DEFAULT_CALENDAR_ID
        resolved_location_id = appointment_data.get("location_id") or cls.DEFAULT_LOCATION_ID

        if not resolved_calendar_id:
            raise ValueError("calendar_id es requerido (proporcione en data o GHL_CALENDAR_ID)")
        if not resolved_location_id:
            raise ValueError("location_id es requerido (proporcione en data o GHL_LOCATION_ID)")

        payload = {
            "calendarId": resolved_calendar_id,
            "contactId": appointment_data["contact_id"],
            "locationId": resolved_location_id,
            "startTime": appointment_data["start_time"],
            "endTime": appointment_data["end_time"],
            "title": appointment_data.get("title") or "Appointment",
            # Opcionales soportados por GHL si se desea:
            # "notes": appointment_data.get("notes"),
            # "assignedUserId": appointment_data.get("assigned_user_id"),
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()