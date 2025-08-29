from rest_framework import serializers
from .user import UserSerializer
from ..models.user import User


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer para lectura del perfil de usuario"""
    
    completion_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'user_name', 'name', 'paternal_lastname', 'maternal_lastname',
            'sex', 'email', 'phone', 'photo_url', 'document_number', 'document_type',
            'country', 'account_statement', 'is_active', 'date_joined', 'last_login',
            'completion_percentage'
        ]
        read_only_fields = ['id', 'user_name', 'date_joined', 'last_login', 'account_statement']
    
    def get_completion_percentage(self, obj):
        """Retorna el porcentaje de completitud del perfil"""
        required_fields = ['name', 'email', 'phone']
        completed_fields = sum(1 for field in required_fields if getattr(obj, field))
        return (completed_fields / len(required_fields)) * 100


class ProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear un perfil de usuario"""
    
    class Meta:
        model = User
        fields = [
            'name', 'paternal_lastname', 'maternal_lastname',
            'sex', 'email', 'phone', 'document_number', 'document_type', 'country'
        ]
    
    def validate_email(self, value):
        """Validación personalizada para el email"""
        # Verificar que el email no esté en uso por otro usuario
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado")
        return value
    
    def create(self, validated_data):
        """Crea un nuevo perfil de usuario"""
        user = self.context['request'].user
        for attr, value in validated_data.items():
            setattr(user, attr, value)
        user.save()
        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar el perfil de usuario"""
    
    class Meta:
        model = User
        fields = [
            'name', 'paternal_lastname', 'maternal_lastname',
            'sex', 'email', 'phone', 'document_number', 'document_type', 'country'
        ]
    
    def validate_email(self, value):
        """Validación personalizada para el email"""
        user = self.context['request'].user
        # Verificar que el email no esté en uso por otro usuario (excluyendo el actual)
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Este email ya está registrado")
        return value
    
    def update(self, instance, validated_data):
        """Actualiza la instancia del perfil"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PublicProfileSerializer(serializers.ModelSerializer):
    """Serializer para perfiles públicos (sin información sensible)"""
    
    display_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'user_name', 'display_name', 'sex', 'country',
            'photo_url', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def get_display_name(self, obj):
        """Retorna el nombre para mostrar"""
        return f"{obj.name} {obj.paternal_lastname}".strip()


class ProfileSettingsSerializer(serializers.ModelSerializer):
    """Serializer para configuraciones del perfil"""
    
    class Meta:
        model = User
        fields = [
            'account_statement'
        ]
    
    def update(self, instance, validated_data):
        """Actualiza solo las configuraciones del perfil"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
