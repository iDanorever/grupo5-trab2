from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from ..models.user import User

User = get_user_model()

class ProfileService:
    """
    Servicio para gestión de perfiles de usuario.
    """
    
    @staticmethod
    def create_profile(user, profile_data):
        """
        Crear un perfil para un usuario.
        """
        try:
            with transaction.atomic():
                # Verificar si ya existe un perfil para evitar duplicados
                if hasattr(user, 'profile'):
                    raise ValidationError("El usuario ya tiene un perfil")
                
                # Crear el perfil con los datos proporcionados
                profile = User.objects.create(
                    user=user,
                    **profile_data
                )
                
                return profile
                
        except Exception as e:
            raise ValidationError(f"Error al crear el perfil: {str(e)}")
    
    @staticmethod
    def update_profile(user, profile_data):
        """
        Actualizar el perfil de un usuario.
        """
        try:
            with transaction.atomic():
                profile = user.profile
                
                # Actualizar solo los campos que existen en el modelo
                for field, value in profile_data.items():
                    if hasattr(profile, field):
                        setattr(profile, field, value)
                
                profile.save()
                return profile
                
        except Exception as e:
            raise ValidationError(f"Error al actualizar el perfil: {str(e)}")
    
    @staticmethod
    def get_profile_by_user(user):
        """
        Obtener el perfil de un usuario específico.
        """
        try:
            return user.profile
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_public_profiles():
        """
        Obtener todos los perfiles públicos del sistema.
        """
        return User.objects.filter(is_public=True)
    
    @staticmethod
    def get_profile_by_username(username):
        """
        Obtener perfil de usuario por su nombre de usuario.
        """
        try:
            user = User.objects.get(username=username)
            return user.profile
        except (User.DoesNotExist, User.DoesNotExist):
            return None
    
    @staticmethod
    def calculate_profile_completion(profile):
        """
        Calcular el porcentaje de completitud del perfil.
        """
        # Campos obligatorios que deben estar completos
        required_fields = [
            'first_name', 'paternal_lastname', 'gender', 'email'
        ]
        
        # Campos opcionales que mejoran el perfil
        optional_fields = [
            'maternal_lastname', 'bio', 'website'
        ]
        
        total_fields = len(required_fields) + len(optional_fields)
        completed_fields = 0
        
        # Verificar campos requeridos (peso completo)
        for field in required_fields:
            if getattr(profile, field):
                completed_fields += 1
        
        # Verificar campos opcionales (peso reducido)
        for field in optional_fields:
            if getattr(profile, field):
                completed_fields += 0.5
        
        # Calcular porcentaje y limitar a 100
        return min(100, int((completed_fields / total_fields) * 100))
    
    @staticmethod
    def get_profile_stats(profile):
        """
        Obtener estadísticas completas del perfil.
        """
        return {
            'completion_percentage': ProfileService.calculate_profile_completion(profile),
            'is_complete': profile.is_complete(),
            'is_public': profile.is_public,
            'show_email': profile.show_email,
            'show_phone': profile.show_phone,
            'receive_notifications': profile.receive_notifications
        }
    
    @staticmethod
    def toggle_profile_visibility(profile):
        """
        Cambiar la visibilidad del perfil entre público y privado.
        """
        # Alternar el estado de visibilidad
        profile.is_public = not profile.is_public
        profile.save()
        return profile
    
    @staticmethod
    def update_privacy_settings(profile, privacy_data):
        """
        Actualizar las configuraciones de privacidad del perfil.
        """
        # Campos de privacidad válidos para actualizar
        privacy_fields = ['show_email', 'show_phone', 'receive_notifications']
        
        # Actualizar solo los campos de privacidad válidos
        for field in privacy_fields:
            if field in privacy_data:
                setattr(profile, field, privacy_data[field])
        
        profile.save()
        return profile