import re
from datetime import date
from rest_framework import serializers
from therapists.models import Therapist 
from ubi_geo.models import Region, Province, District
from ubi_geo.serializers import RegionSerializer, ProvinceSerializer, DistrictSerializer
from histories_configurations.models import DocumentType
from histories_configurations.serializers import DocumentTypeSerializer

class TherapistSerializer(serializers.ModelSerializer):
    # Serializadores anidados para mostrar datos completos
    region_fk = RegionSerializer(read_only=True)
    province_fk = ProvinceSerializer(read_only=True)
    district_fk = DistrictSerializer(read_only=True)
    document_type = DocumentTypeSerializer(read_only=True)  # Para lectura
    
    # Campos para escritura (crear/actualizar)
    region_fk_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(), 
        source='region_fk', 
        allow_null=True, 
        required=False,
        write_only=True
    )
    province_fk_id = serializers.PrimaryKeyRelatedField(
        queryset=Province.objects.all(), 
        source='province_fk', 
        allow_null=True, 
        required=False,
        write_only=True
    )
    district_fk_id = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(), 
        source='district_fk', 
        allow_null=True, 
        required=False,
        write_only=True
    )
    document_type_id = serializers.PrimaryKeyRelatedField(
        queryset=DocumentType.objects.all(),
        source='document_type',
        write_only=True,
        error_messages={
            'does_not_exist': 'El tipo de documento seleccionado no existe.'
        }
    )

    class Meta:
        model = Therapist
        fields = "__all__"
        extra_kwargs = {
            'email': {
                'required': False,
                'allow_null': True,
                'error_messages': {
                    'invalid': "El correo debe ser válido y terminar en @gmail.com"
                }
            }
        }
        
    def validate(self, attrs):
        """
        Asegura coherencia jerárquica:
        province_fk debe pertenecer a region_fk
        district_fk debe pertenecer a province_fk
        """
        region = attrs.get("region_fk") or getattr(self.instance, "region_fk", None)
        province = attrs.get("province_fk") or getattr(self.instance, "province_fk", None)
        district = attrs.get("district_fk") or getattr(self.instance, "district_fk", None)

        if province and region and province.region_id != region.id:
            raise serializers.ValidationError(
                "La provincia seleccionada no pertenece a la región."
            )
        if district and province and district.province_id != province.id:
            raise serializers.ValidationError(
                "El distrito seleccionado no pertenece a la provincia."
            )
        return attrs

    def validate_document_number(self, value):
        # Obtener el tipo de documento desde los datos iniciales o la instancia
        doc_type_id = self.initial_data.get("document_type_id")
        
        # Si no está en initial_data, intentar obtener de la instancia existente
        if not doc_type_id and self.instance:
            doc_type_id = self.instance.document_type_id
        
        if not doc_type_id:
            return value  # No podemos validar sin tipo de documento
        
        # Obtener el nombre del tipo de documento para las validaciones
        try:
            document_type = DocumentType.objects.get(id=doc_type_id)
            doc_type_name = document_type.name.upper()
        except DocumentType.DoesNotExist:
            # La validación de existencia se hará en document_type_id field
            return value

        # Validaciones según el tipo de documento
        if doc_type_name == "DNI":
            if not value.isdigit():
                raise serializers.ValidationError("El DNI debe contener solo números.")
            if not (8 <= len(value) <= 9):
                raise serializers.ValidationError(
                    "El DNI debe tener entre 8 y 9 dígitos."
                )

        elif doc_type_name == "CE" or "CARNE DE EXTRANJERIA" in doc_type_name:
            if not value.isdigit():
                raise serializers.ValidationError(
                    "El Carné de Extranjería debe contener solo números."
                )
            if len(value) > 12:
                raise serializers.ValidationError(
                    "El Carné de Extranjería debe tener máximo 12 dígitos."
                )

        elif doc_type_name == "PTP":
            if not value.isdigit():
                raise serializers.ValidationError("El PTP debe contener solo números.")
            if len(value) != 9:
                raise serializers.ValidationError(
                    "El PTP debe tener exactamente 9 dígitos."
                )

        elif doc_type_name == "CR" or "CARNE DE REFUGIADO" in doc_type_name:
            if not re.match(r"^[A-Za-z0-9]+$", value):
                raise serializers.ValidationError(
                    "El Carné de Refugiado debe contener solo letras y números."
                )

        elif doc_type_name == "PAS" or "PASAPORTE" in doc_type_name:
            if not re.match(r"^[A-Za-z0-9]+$", value):
                raise serializers.ValidationError(
                    "El Pasaporte debe contener solo letras y números."
                )

        return value

    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value

    def validate_last_name_paternal(self, value):
        if not value.strip():
            raise serializers.ValidationError("El apellido paterno no puede estar vacío.")
        return value

    def validate_last_name_maternal(self, value):
        # Este campo puede ser null/blank, pero si tiene valor debe ser válido
        if value and not value.strip():
            raise serializers.ValidationError("El apellido materno no puede estar vacío.")
        return value

    def validate_personal_reference(self, value):
        if value and not re.match(r"^[A-Za-z0-9\s]+$", value):
            raise serializers.ValidationError(
                "La referencia personal solo puede contener letras y números."
            )
        return value

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El teléfono debe contener solo dígitos.")
        if len(value) > 15:
            raise serializers.ValidationError(
                "El teléfono debe tener máximo 15 dígitos."
            )
        return value

    def validate_email(self, value):
        if value:
            pattern = r'^[A-Za-z0-9._%+-]+@gmail\.com$'
            if not re.match(pattern, value):
                raise serializers.ValidationError("El correo debe ser válido y terminar en @gmail.com (ejemplo: usuario@gmail.com).")
        return value

    def validate_birth_date(self, value):
        today = date.today()

        # No permitir fechas futuras
        if value > today:
            raise serializers.ValidationError("La fecha de nacimiento no puede ser futura.")

        # Calcular edad
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("El terapeuta debe tener al menos 18 años.")

        return value

    def validate_profile_picture(self, value):
        if not value:
            return value
        valid_extensions = ["png", "jpg", "jpeg"]
        ext = str(value).split(".")[-1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError(
                "La imagen debe estar en formato PNG, JPG o JPEG."
            )
        return value