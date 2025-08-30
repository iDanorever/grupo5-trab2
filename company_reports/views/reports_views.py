from django.http import JsonResponse, HttpResponse
from company_reports.services.reports_services import ReportService
from company_reports.serialiazers.reports_serializers import (
    DateParameterSerializer,
    TherapistAppointmentSerializer,
    PatientByTherapistSerializer,
    DailyCashSerializer,
    AppointmentRangeSerializer,
    PDFContextSerializer,
)
from django.shortcuts import render
# from django_xhtml2pdf.utils import pdf_decorator
from django.views.decorators.csrf import csrf_exempt
import xlsxwriter
import io
import json

report_service = ReportService()


# --------- Helpers ---------
def _merge_params(request):
    """
    Mezcla query params y body (JSON o form) para soportar GET y POST.
    - Los valores del body tienen prioridad sobre los de la query string.
    """
    merged = {}

    # Query params
    for k, v in request.GET.items():
        merged[k] = v

    # Body (POST/PUT/PATCH)
    if request.method in ("POST", "PUT", "PATCH"):
        if request.content_type and "application/json" in request.content_type:
            try:
                body = json.loads(request.body or b"{}")
                if isinstance(body, dict):
                    merged.update(body)
            except json.JSONDecodeError:
                pass
        else:
            for k, v in request.POST.items():
                merged[k] = v

    return merged


# ===========================
#   JSON API
# ===========================
class ReportAPIView:
    """Responsable exclusivamente de endpoints JSON de reportes."""

    @staticmethod
    def get_number_appointments_per_therapist(request):
        """
        Devuelve JSON con el número de citas por terapeuta para una fecha dada.
        GET  /...?date=YYYY-MM-DD
        POST /... con body {"date":"YYYY-MM-DD"} o ?date=...
        """
        # Validar parámetros (mezcla GET + body)
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        # Obtener datos usando parámetros validados
        data = report_service.get_appointments_count_by_therapist(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        # Serializar respuesta (con porcentaje)
        response_serializer = TherapistAppointmentSerializer(
            data["therapists_appointments"],
            many=True,
            context={"total_appointments": data["total_appointments_count"]},
        )

        return JsonResponse(
            {
                "date": str(serializer.validated_data.get("date")),
                "therapists_appointments": response_serializer.data,
                "total_appointments_count": data["total_appointments_count"],
            }
        )

    @staticmethod
    def get_patients_by_therapist(request):
        """Devuelve JSON con los pacientes agrupados por terapeuta para una fecha dada."""
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_patients_by_therapist(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        response_serializer = PatientByTherapistSerializer(data, many=True)
        return JsonResponse(response_serializer.data, safe=False)

    @staticmethod
    def get_daily_cash(request):
        """Devuelve JSON con el resumen diario de efectivo agrupado por tipo de pago."""
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_daily_cash(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        response_serializer = DailyCashSerializer(data, many=True)
        return JsonResponse(response_serializer.data, safe=False)

    @staticmethod
    def get_appointments_between_dates(request):
        """Devuelve JSON con todas las citas entre dos fechas con info de paciente y terapeuta."""
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_appointments_between_dates(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        response_serializer = AppointmentRangeSerializer(data, many=True)
        return JsonResponse(response_serializer.data, safe=False)


# ===========================
#   PDF
# ===========================
class PDFExportView:
    """Responsable exclusivamente de la generación de PDFs."""

    @staticmethod
    # @pdf_decorator(pdfname="citas_terapeuta.pdf")
    def pdf_citas_terapeuta(request):
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_appointments_count_by_therapist(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        context_data = {
            "date": serializer.validated_data.get("date"),
            "data": data,
            "title": "Citas por Terapeuta",
        }
        context_serializer = PDFContextSerializer(context_data)
        context = context_serializer.data
        return render(request, "pdf_templates/citas_terapeuta.html", context)

    @staticmethod
    # @pdf_decorator(pdfname="pacientes_por_terapeuta.pdf")
    def pdf_pacientes_terapeuta(request):
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_patients_by_therapist(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        context_data = {
            "date": serializer.validated_data.get("date"),
            "data": data,
            "title": "Pacientes por Terapeuta",
        }
        context_serializer = PDFContextSerializer(context_data)
        context = context_serializer.data
        return render(request, "pdf_templates/pacientes_terapeuta.html", context)

    @staticmethod
    # @pdf_decorator(pdfname="resumen_caja.pdf")
    def pdf_resumen_caja(request):
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_daily_cash(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        # Calcular total correcto (sumando 'payment')
        total = sum(float(item.get("payment", 0) or 0) for item in data) if data else 0.0

        context_data = {
            "date": serializer.validated_data.get("date"),
            "data": data,
            "total": total,
            "title": "Resumen de Caja Diaria",
        }
        context_serializer = PDFContextSerializer(context_data)
        context = context_serializer.data
        return render(request, "pdf_templates/resumen_caja.html", context)


# ===========================
#   Excel
# ===========================
class ExcelExportView:
    """Responsable exclusivamente de la exportación a Excel."""

    @staticmethod
    def exportar_excel_citas(request):
        data_in = _merge_params(request)
        serializer = DateParameterSerializer(data=data_in)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        data = report_service.get_appointments_between_dates(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)

        # Crear archivo Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("Citas")

        # Formato encabezado
        header_format = workbook.add_format(
            {"bold": True, "bg_color": "#2c3e50", "font_color": "white", "border": 1}
        )

        # Encabezados alineados con AppointmentRangeSerializer
        headers = [
            "ID Paciente",
            "DNI/Documento",
            "Paciente",
            "Teléfono",
            "Fecha",
            "Hora",
        ]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        # Escribir datos
        for row, appointment in enumerate(data, start=1):
            worksheet.write(row, 0, appointment.get("patient_id", ""))
            worksheet.write(row, 1, appointment.get("document_number_patient", ""))
            worksheet.write(row, 2, appointment.get("patient", ""))
            worksheet.write(row, 3, appointment.get("phone1_patient", ""))
            worksheet.write(row, 4, appointment.get("appointment_date", ""))
            worksheet.write(row, 5, appointment.get("hour", ""))

        # Anchos de columna
        worksheet.set_column("A:A", 12)
        worksheet.set_column("B:B", 15)
        worksheet.set_column("C:C", 40)
        worksheet.set_column("D:D", 15)
        worksheet.set_column("E:E", 12)
        worksheet.set_column("F:F", 10)

        workbook.close()
        output.seek(0)

        # Nombre de archivo (si hay rango en query)
        start_date = serializer.validated_data.get("start_date")
        end_date = serializer.validated_data.get("end_date")
        if start_date and end_date:
            filename = f"citas_{start_date}_a_{end_date}.xlsx"
        else:
            filename = "citas.xlsx"

        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response


# ===========================
#   Wrappers (compatibilidad) + CSRF EXEMPT PARA TESTEAR POST EN POSTMAN
# ===========================
report_api = ReportAPIView()
pdf_export = PDFExportView()
excel_export = ExcelExportView()


@csrf_exempt
def get_number_appointments_per_therapist(request):
    try:
        return report_api.get_number_appointments_per_therapist(request)
    except Exception as e:
        import traceback

        print(f"Error en get_number_appointments_per_therapist: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse(
            {"error": f"Error interno del servidor: {str(e)}", "traceback": traceback.format_exc()},
            status=500,
        )


@csrf_exempt
def get_patients_by_therapist(request):
    try:
        return report_api.get_patients_by_therapist(request)
    except Exception as e:
        import traceback

        print(f"Error en get_patients_by_therapist: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse(
            {"error": f"Error interno del servidor: {str(e)}", "traceback": traceback.format_exc()},
            status=500,
        )


@csrf_exempt
def get_daily_cash(request):
    try:
        return report_api.get_daily_cash(request)
    except Exception as e:
        import traceback

        print(f"Error en get_daily_cash: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse(
            {"error": f"Error interno del servidor: {str(e)}", "traceback": traceback.format_exc()},
            status=500,
        )


@csrf_exempt
def get_appointments_between_dates(request):
    try:
        return report_api.get_appointments_between_dates(request)
    except Exception as e:
        import traceback

        print(f"Error en get_appointments_between_dates: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse(
            {"error": f"Error interno del servidor: {str(e)}", "traceback": traceback.format_exc()},
            status=500,
        )


def reports_dashboard(request):
    return render(request, "reports.html")


def pdf_citas_terapeuta(request):
    return pdf_export.pdf_citas_terapeuta(request)


def pdf_pacientes_terapeuta(request):
    return pdf_export.pdf_pacientes_terapeuta(request)


def pdf_resumen_caja(request):
    return pdf_export.pdf_resumen_caja(request)


def exportar_excel_citas(request):
    return excel_export.exportar_excel_citas(request)
