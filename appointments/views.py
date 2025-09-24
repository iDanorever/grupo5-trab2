from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Cita
from .serializers import CitaSerializer
from .services import crear_cita_en_ghl

@api_view(["POST"]) 
def crear_cita(request):
    serializer = CitaSerializer(data=request.data)

    if serializer.is_valid():
        cita = serializer.save()  # Guarda la cita localmente

        # El frontend puede mandar contact_id si ya existe el contacto en GHL
        contact_id = request.data.get("contact_id")

        if not contact_id:
            return Response({"error": "Falta contact_id"}, status=400)

        try:
            # Enviar cita a GHL
            data = crear_cita_en_ghl(cita, contact_id)

#Guardar el ID de la cita en GHL en la DB local
            cita.appointment_id_ghl = data.get("id")
            cita.save()

            return Response(
                {
                    "msg": "✅ Cita creada y enviada a GHL",
                    "cita": CitaSerializer(cita).data,
                    "ghl_respuesta": data,
                }, status=status.HTTP_201_CREATED,)



        except Exception as e:
            # Si falla en GHL, eliminamos la cita local
            cita.delete()
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    # Si la validación del serializer falla
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)