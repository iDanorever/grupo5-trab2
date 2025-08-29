from datetime import datetime
from django.utils.timezone import localtime
from django.db.models import Count, Q, CharField, Value
from django.db.models.functions import Concat, TruncDate
from appointments_status.models.appointment import Appointment
from therapists.models.therapist import Therapist


# from django.db import models  # 👈 no se usa

class ReportService:
    def get_appointments_count_by_therapist(self, validated_data):
        """
        Conteo de TODAS las citas por terapeuta para una fecha dada.
        Agrupa desde Appointment para evitar problemas de related_name.
        """
        query_date = validated_data.get("date")

        # Si appointment_date es DateField, basta con igualdad.
        # Si es DateTimeField, usamos TruncDate para comparar el día.
        # Esta versión funciona en ambos casos (TruncDate ⇒ date-only).
        qs = (
            Appointment.objects
            .filter(therapist__isnull=False)
            .annotate(day=TruncDate("appointment_date"))
            .filter(day=query_date)
            .values(
                "therapist_id",
                "therapist__first_name",
                "therapist__last_name_paternal",
                "therapist__last_name_maternal",
            )
            .annotate(appointments_count=Count("id"))
        )

        therapists = [
            {
                "id": row["therapist_id"],
                "name": f'{row["therapist__first_name"]} {row["therapist__last_name_paternal"] or ""} {row["therapist__last_name_maternal"] or ""}'.strip(),
                "last_name_paternal": row["therapist__last_name_paternal"],
                "last_name_maternal": row["therapist__last_name_maternal"],
                "appointments_count": row["appointments_count"],
            }
            for row in qs
        ]

        # Ordenar por mayor número de citas (como antes)
        therapists.sort(key=lambda t: (-t["appointments_count"], t["last_name_paternal"] or "", t["last_name_maternal"] or "", t["id"]))

        total_appointments = sum(t["appointments_count"] for t in therapists)

        return {
            "therapists_appointments": therapists,
            "total_appointments_count": total_appointments,
        }

    def get_patients_by_therapist(self, validated_data):
        """Pacientes agrupados por terapeuta para una fecha dada."""
        query_date = validated_data.get("date")

        appointments = (
            Appointment.objects
            .select_related("patient", "therapist")
            .annotate(day=TruncDate("appointment_date"))
            .filter(day=query_date)
        )

        report = {}
        sin_terapeuta = {
            "therapist_id": "",
            "therapist": "Sin terapeuta asignado",
            "patients": {}
        }

        for appointment in appointments:
            patient = appointment.patient
            therapist = appointment.therapist
            if not patient:
                continue

            patient_data = {
                "patient_id": patient.id,
                "patient": f"{patient.paternal_lastname} {patient.maternal_lastname or ''} {patient.name}".strip(),
                "appointments": 0,
            }

            if not therapist:
                key = patient.id
                if key not in sin_terapeuta["patients"]:
                    sin_terapeuta["patients"][key] = patient_data
                sin_terapeuta["patients"][key]["appointments"] += 1
            else:
                t_id = therapist.id
                if t_id not in report:
                    report[t_id] = {
                        "therapist_id": t_id,
                        # usa first_name (no existe 'name' en el modelo)
                        "therapist": f"{therapist.last_name_paternal} {therapist.last_name_maternal or ''} {therapist.first_name}".strip(),
                        "patients": {}
                    }
                key = patient.id
                if key not in report[t_id]["patients"]:
                    report[t_id]["patients"][key] = patient_data
                report[t_id]["patients"][key]["appointments"] += 1

        # Agregar grupo “sin terapeuta” si aplica
        if sin_terapeuta["patients"]:
            report["sinTherapist"] = sin_terapeuta

        # Convertir dicts de pacientes a listas
        for therapist_id in list(report.keys()):
            report[therapist_id]["patients"] = list(report[therapist_id]["patients"].values())

        return list(report.values())

    def get_daily_cash(self, validated_data):
        """Resumen diario de efectivo detallado por cita."""
        query_date = validated_data.get("date")

        payments = (
            Appointment.objects
            .filter(
                appointment_date=query_date,
                payment__isnull=False,
                payment_type__isnull=False
            )
            .values(
                'id',
                'payment',
                'payment_type',
                'payment_type__name'
            )
            .order_by('-id')
        )

        result = [
            {
                "id_cita": p['id'],
                "payment": p['payment'],
                "payment_type": p['payment_type'],
                "payment_type_name": p['payment_type__name']
            }
            for p in payments
        ]
        return result

    def get_appointments_between_dates(self, validated_data):
        """Citas entre dos fechas dadas."""
        start_date = validated_data.get("start_date")
        end_date = validated_data.get("end_date")

        appointments = (
            Appointment.objects
            .select_related("patient", "therapist")
            .filter(
                appointment_date__gte=start_date,
                appointment_date__lte=end_date
            )
            .order_by("appointment_date", "hour")
        )

        result = []
        for app in appointments:
            if not app.patient:
                continue

            patient_name = " ".join(filter(None, [
                app.patient.paternal_lastname,
                app.patient.maternal_lastname,
                app.patient.name
            ]))

            hour_val = app.hour
            hour_str = hour_val if isinstance(hour_val, str) else (hour_val.strftime("%H:%M") if hour_val else "")

            result.append({
                "appointment_id": app.id,
                "patient_id": app.patient.id,
                "document_number_patient": app.patient.document_number,
                "patient": patient_name,
                "phone1_patient": app.patient.phone1,
                "appointment_date": app.appointment_date.strftime("%Y-%m-%d"),
                "hour": hour_str,
            })

        return result
