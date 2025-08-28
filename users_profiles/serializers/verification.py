from rest_framework import serializers
from ..models.user_verification_code import UserVerificationCode

class VerificationCodeSerializer(serializers.ModelSerializer):
    """Serializer para códigos de verificación del modelo UserVerificationCode"""
    
    class Meta:
        model = UserVerificationCode
        fields = ['code', 'verification_type', 'target_email']
    
    def validate_code(self, value):
        """Valida el formato del código de verificación
        
        Args:
            value (str): Código de verificación a validar
            
        Returns:
            str: Código validado
            
        Raises:
            ValidationError: Si el código no tiene 6 dígitos numéricos
        """
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("El código debe ser de 6 dígitos")
        return value

class EmailChangeSerializer(serializers.Serializer):
    """Serializer para solicitar cambio de email"""
    
    new_email = serializers.EmailField(
        help_text='Nuevo email para la cuenta'
    )
    
    def validate_new_email(self, value):
        """Valida que el nuevo email no esté en uso por otro usuario
        
        Args:
            value (str): Nuevo email a validar
            
        Returns:
            str: Email validado
            
        Raises:
            ValidationError: Si el email ya está registrado
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado")
        
        return value

class EmailChangeConfirmSerializer(serializers.Serializer):
    """Serializer para confirmar cambio de email con código de verificación"""
    
    code = serializers.CharField(
        max_length=6,
        help_text='Código de verificación de 6 dígitos'
    )
    
    def validate_code(self, value):
        """Valida el formato del código de confirmación
        
        Args:
            value (str): Código de confirmación a validar
            
        Returns:
            str: Código validado
            
        Raises:
            ValidationError: Si el código no tiene 6 dígitos numéricos
        """
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("El código debe ser de 6 dígitos")
        return value

class VerificationCodeRequestSerializer(serializers.Serializer):
    """Serializer para solicitar un código de verificación"""
    
    verification_type = serializers.ChoiceField(
        choices=UserVerificationCode.VERIFICATION_TYPES,
        help_text='Tipo de verificación requerida'
    )
    
    target_email = serializers.EmailField(
        required=False,
        help_text='Email objetivo (requerido para cambio de email)'
    )
    
    def validate(self, attrs):
        """Validación personalizada para la solicitud de código
        
        Verifica que se proporcione el email objetivo cuando el tipo
        de verificación sea cambio de email.
        
        Args:
            attrs (dict): Datos validados
            
        Returns:
            dict: Datos validados
            
        Raises:
            ValidationError: Si falta el email objetivo para cambio de email
        """
        verification_type = attrs.get('verification_type')
        target_email = attrs.get('target_email')
        
        if verification_type == 'email_change' and not target_email:
            raise serializers.ValidationError(
                "El email objetivo es requerido para cambio de email"
            )
        
        return attrs

class VerificationCodeResendSerializer(serializers.Serializer):
    """Serializer para reenviar código de verificación"""
    
    verification_type = serializers.ChoiceField(
        choices=UserVerificationCode.VERIFICATION_TYPES,
        help_text='Tipo de verificación'
    )
    
    target_email = serializers.EmailField(
        required=False,
        help_text='Email objetivo (para cambio de email)'
    )

class VerificationStatusSerializer(serializers.Serializer):
    """Serializer para mostrar el estado de verificación (solo lectura)"""
    
    is_verified = serializers.BooleanField(
        read_only=True,
        help_text='Indica si la verificación fue exitosa'
    )
    
    message = serializers.CharField(
        read_only=True,
        help_text='Mensaje descriptivo del resultado'
    )
    
    expires_at = serializers.DateTimeField(
        read_only=True,
        help_text='Fecha de expiración del código'
    )
    
    attempts_remaining = serializers.IntegerField(
        read_only=True,
        help_text='Intentos restantes para usar el código'
    )

class EmailVerificationSerializer(serializers.Serializer):
    """Serializer para verificación de email de registro"""
    
    email = serializers.EmailField(
        help_text='Email a verificar'
    )
    
    def validate_email(self, value):
        """Valida que el email exista y no esté verificado
        
        Args:
            value (str): Email a validar
            
        Returns:
            str: Email validado
            
        Raises:
            ValidationError: Si el email no existe o ya está verificado
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            user = User.objects.get(email=value)
            if user.email_verified:
                raise serializers.ValidationError("Este email ya está verificado")
        except User.DoesNotExist:
            raise serializers.ValidationError("No existe una cuenta con este email")
        
        return value