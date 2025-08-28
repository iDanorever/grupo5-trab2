from rest_framework import serializers
from .user import UserSerializer
from ..models.user import User

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer para lectura completa del perfil de usuario.
    
    Incluye información del usuario relacionado y el porcentaje de completitud.
    Usado principalmente para mostrar el perfil completo al propietario.
    """
    
    user = UserSerializer(read_only=True)  # Información del usuario asociado
    completion_percentage = serializers.SerializerMethodField()  # Porcentaje calculado
    
    class Meta:
        model = User
        fields = [
            'id', 'user', 'first_name', 'paternal_lastname', 'maternal_lastname',
            'gender', 'email', 'is_public', 'show_email', 'show_phone',
            'receive_notifications', 'created_at', 'updated_at', 'completion_percentage'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_completion_percentage(self, obj):
        """Calcula y retorna el porcentaje de completitud del perfil."""
        return obj.get_completion_percentage()


class ProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear un nuevo perfil de usuario.
    
    Valida que el email no esté duplicado y asocia automáticamente
    el perfil al usuario autenticado.
    """
    
    class Meta:
        model = User
        fields = [
            'first_name', 'paternal_lastname', 'maternal_lastname',
            'gender', 'email', 'is_public', 'show_email', 'show_phone',
            'receive_notifications'
        ]
    
    def validate_email(self, value):
        """Valida que el email no esté registrado en otro perfil."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado en otro perfil")
        return value
    
    def create(self, validated_data):
        """Crea un nuevo perfil asociado al usuario autenticado."""
        user = self.context['request'].user
        profile = User.objects.create(user=user, **validated_data)
        return profile


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar un perfil existente.
    
    Permite actualizar todos los campos del perfil excepto el usuario asociado.
    Valida que el email no esté en uso por otro perfil.
    """
    
    class Meta:
        model = User
        fields = [
            'first_name', 'paternal_lastname', 'maternal_lastname',
            'gender', 'email', 'is_public', 'show_email', 'show_phone',
            'receive_notifications'
        ]
    
    def validate_email(self, value):
        """Valida que el email no esté en uso por otro perfil."""
        user = self.context['request'].user
        # Excluir el perfil actual de la validación
        if User.objects.filter(email=value).exclude(user=user).exists():
            raise serializers.ValidationError("Este email ya está registrado en otro perfil")
        return value
    
    def update(self, instance, validated_data):
        """Actualiza los campos del perfil."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PublicProfileSerializer(serializers.ModelSerializer):
    """Serializer para perfiles públicos sin información sensible.
    
    Filtra automáticamente la información según las configuraciones de privacidad
    del usuario. Usado para mostrar perfiles a otros usuarios.
    """
    
    user = serializers.SerializerMethodField()  # Info básica del usuario
    display_name = serializers.SerializerMethodField()  # Nombre para mostrar
    
    class Meta:
        model = User
        fields = [
            'id', 'user', 'display_name', 'gender', 'country', 'city',
            'website', 'bio', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_user(self, obj):
        """Retorna información básica y segura del usuario."""
        user_data = {
            'username': obj.user.username,
            'profile_photo_url': None
        }
        
        # Construir URL absoluta de la foto de perfil si existe
        if obj.user.profile_photo:
            request = self.context.get('request')
            if request:
                user_data['profile_photo_url'] = request.build_absolute_uri(obj.user.profile_photo.url)
            else:
                user_data['profile_photo_url'] = obj.user.profile_photo.url
        
        return user_data
    
    def get_display_name(self, obj):
        """Retorna el nombre para mostrar públicamente."""
        return obj.get_display_name()
    
    def to_representation(self, instance):
        """Personaliza la representación según configuraciones de privacidad."""
        data = super().to_representation(instance)
        
        # Filtrar email según configuración de privacidad
        if not instance.show_email:
            data.pop('email', None)
        
        # Filtrar teléfono según configuración de privacidad
        if not instance.show_phone:
            data.pop('phone_number', None)
        
        return data


class ProfileSettingsSerializer(serializers.ModelSerializer):
    """Serializer para configuraciones de privacidad del perfil.
    
    Permite actualizar únicamente las configuraciones de visibilidad
    y notificaciones sin afectar otros datos del perfil.
    """
    
    class Meta:
        model = User
        fields = [
            'is_public', 'show_email', 'show_phone', 'receive_notifications'
        ]
    
    def update(self, instance, validated_data):
        """Actualiza solo las configuraciones de privacidad."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance