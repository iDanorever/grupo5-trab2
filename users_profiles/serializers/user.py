from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer para lectura completa del modelo User.
    
    Incluye campos calculados como nombre completo y URL de foto de perfil.
    Usado principalmente para mostrar información del usuario.
    """
    
    full_name = serializers.SerializerMethodField()  # Nombre completo calculado
    profile_photo_url = serializers.SerializerMethodField()  # URL de foto de perfil
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'phone', 'rol', 'is_active', 'date_joined', 'last_login',
            'profile_photo_url'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'last_login', 'rol']
    
    def get_full_name(self, obj):
        """Retorna el nombre completo del usuario."""
        return obj.get_full_name()
    
    def get_profile_photo_url(self, obj):
        """Retorna la URL absoluta de la foto de perfil."""
        if obj.profile_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_photo.url)
            return obj.profile_photo.url
        return None

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualización de datos básicos del usuario.
    
    Permite actualizar nombre, apellido y teléfono.
    No incluye campos sensibles como email o username.
    """
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone'
        ]
    
    def validate_phone(self, value):
        """Valida el formato del número de teléfono."""
        if value:
            # Validación básica de longitud mínima
            if len(value) < 7:
                raise serializers.ValidationError("El número de teléfono debe tener al menos 7 dígitos")
        return value
    
    def update(self, instance, validated_data):
        """Actualiza los campos básicos del usuario."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer para registro de nuevos usuarios.
    
    Incluye validación de contraseñas, verificación de unicidad
    de email y username, y creación segura del usuario.
    """
    
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],  # Validación de Django para contraseñas
        help_text='La contraseña debe cumplir con los requisitos de seguridad'
    )
    
    password_confirm = serializers.CharField(
        write_only=True,
        help_text='Confirma tu contraseña'
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name'
        ]
    
    def validate(self, attrs):
        """Validación completa para el registro de usuario."""
        # Verificar que las contraseñas coincidan
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        
        # Verificar unicidad del email
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Este email ya está registrado")
        
        # Verificar unicidad del username
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso")
        
        return attrs
    
    def create(self, validated_data):
        """Crea un nuevo usuario con contraseña encriptada."""
        validated_data.pop('password_confirm')  # Remover confirmación
        user = User.objects.create_user(**validated_data)
        return user

class UserProfilePhotoSerializer(serializers.ModelSerializer):
    """Serializer para actualización de la foto de perfil del usuario.
    
    Maneja la subida de imágenes y eliminación de fotos anteriores
    para evitar acumulación de archivos no utilizados.
    """
    
    profile_photo = serializers.ImageField(
        max_length=None,
        allow_empty_file=False,  # No permitir archivos vacíos
        use_url=True  # Retornar URL en lugar del archivo
    )
    
    class Meta:
        model = User
        fields = ['profile_photo']
    
    def update(self, instance, validated_data):
        """Actualiza la foto de perfil eliminando la anterior."""
        # Eliminar la foto anterior para liberar espacio
        if instance.profile_photo:
            instance.profile_photo.delete(save=False)
        
        # Asignar la nueva foto
        instance.profile_photo = validated_data['profile_photo']
        instance.save()
        return instance