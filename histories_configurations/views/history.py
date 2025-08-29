import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from ..models.history import History
from ..models.document_type import DocumentType

@csrf_exempt
def histories_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    
    qs = History.objects.filter(deleted_at__isnull=True).select_related("patient")
    data = [{
        "id": h.id,
        "patient": h.patient_id,
        "patient_name": f"{h.patient.name} {h.patient.paternal_lastname}" if h.patient else None
    } for h in qs]
    return JsonResponse({"histories": data})


@csrf_exempt
def history_create(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    # Manejo de JSON inválido
    try:
        payload = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    
    patient_id = payload.get("patient")

    # Validar campos obligatorios
    if patient_id is None:
        return JsonResponse({"error": "Campos obligatorios faltantes"}, status=400)

    # Verificar si ya existe un historial activo para este paciente
    existing_history = History.objects.filter(
        patient_id=patient_id,
        deleted_at__isnull=True
    ).first()
    
    if existing_history:
        return JsonResponse({
            "error": "Ya existe un historial activo para este paciente",
            "existing_history_id": existing_history.id
        }, status=409)
    
    try:
        h = History.objects.create(patient_id=patient_id)
        return JsonResponse({"id": h.id}, status=201)
    except Exception as e:
        return JsonResponse({"error": "Error al crear el historial"}, status=500)

@csrf_exempt
def history_delete(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    try:
        h = History.objects.filter(deleted_at__isnull=True).get(pk=pk)
    except History.DoesNotExist:
        return JsonResponse({"error":"No encontrado"}, status=404)
    
    h.soft_delete()  # Debe marcar deleted_at = timezone.now()
    return JsonResponse({"status": "deleted"})