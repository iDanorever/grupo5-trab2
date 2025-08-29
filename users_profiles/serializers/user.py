from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer para lectura del modelo User"""
    
    full_name = serializers.SerializerMethodField()
    profile_photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'user_name', 'email', 'name', 'paternal_lastname', 'maternal_lastname',
            'full_name', 'phone', 'account_statement', 'is_active', 'date_joined', 'last_login',
            'profile_photo_url', 'document_number', 'document_type', 'sex', 'country', 'photo_url'
        ]
        read_only_fields = ['id', 'user_name', 'date_joined', 'last_login', 'account_statement']
    
    def get_full_name(self, obj):
        """Retorna el nombre completo del usuario"""
        return f"{obj.name} {obj.paternal_lastname} {obj.maternal_lastname}".strip()
    
    def get_profile_photo_url(self, obj):
        """Retorna la URL de la foto de perfil"""
        return obj.photo_url if obj.photo_url else None


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualización del modelo User"""
    
    class Meta:
        model = User
        fields = [
            'name', 'paternal_lastname', 'maternal_lastname', 'phone'
        ]
    
    def validate_phone(self, value):
        """Validación personalizada para el número de teléfono"""
        if value:
            # Validación básica de formato de teléfono
            if len(value) < 7:
                raise serializers.ValidationError("El número de teléfono debe tener al menos 7 dígitos")
        return value
    
    def update(self, instance, validated_data):
        """Actualiza la instancia del usuario"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer para registro de nuevos usuarios"""
    
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        help_text='La contraseña debe cumplir con los requisitos de seguridad'
    )
    
    password_confirm = serializers.CharField(
        write_only=True,
        help_text='Confirma tu contraseña'
    )
    
    class Meta:
        model = User
        fields = [
            'user_name', 'email', 'password', 'password_confirm',
            'name', 'paternal_lastname', 'maternal_lastname'
        ]
    
    def validate(self, attrs):
        """Validación personalizada para el registro"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        
        # Verificar que el email no esté en uso
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Este email ya está registrado")
        
        # Verificar que el username no esté en uso
        if User.objects.filter(user_name=attrs['user_name']).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso")
        
        return attrs
    
    def create(self, validated_data):
        """Crea un nuevo usuario"""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfilePhotoSerializer(serializers.ModelSerializer):
    """Serializer para actualización de la foto de perfil"""
    
    photo_url = serializers.CharField(
        max_length=255,
        help_text='URL de la foto de perfil'
    )
    
    class Meta:
        model = User
        fields = ['photo_url']
    
    def update(self, instance, validated_data):
        """Actualiza la foto de perfil del usuario"""
        instance.photo_url = validated_data['photo_url']
        instance.save()
        return instance
