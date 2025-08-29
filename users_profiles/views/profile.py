# users_profiles/views/profile.py

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

# Django
from django.shortcuts import get_object_or_404
from django.db import models
from django.contrib.auth import get_user_model

# Serializers
from ..serializers.profile import (
    ProfileSerializer, ProfileUpdateSerializer, ProfileCreateSerializer,
    PublicProfileSerializer, ProfileSettingsSerializer
)

User = get_user_model()


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Vista para obtener y actualizar el perfil del usuario autenticado.
    Ahora trabajamos directamente con el CustomUser (AUTH_USER_MODEL).
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Retorna el serializer apropiado según el método HTTP"""
        if self.request.method == 'GET':
            return ProfileSerializer
        return ProfileUpdateSerializer

    def get_object(self):
        """
        Retorna el propio usuario autenticado (no creamos un modelo de perfil aparte).
        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        """Actualiza los datos del usuario"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Perfil actualizado exitosamente',
            'profile': ProfileSerializer(instance, context={'request': request}).data,
        })


class ProfileCreateView(generics.CreateAPIView):
    """
    Vista para crear un 'perfil'.
    Si realmente usas solo el CustomUser, esta vista probablemente no sea necesaria.
    La dejo para compatibilidad, asumiendo que tu serializer crea/actualiza sobre el propio usuario.
    """

    serializer_class = ProfileCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Si tu serializer crea campos adicionales sobre el usuario autenticado,
        puedes implementar la lógica aquí. Por defecto, guardo y no creo nada aparte.
        """
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Asumimos que el serializer trabaja sobre request.user o devuelve datos del usuario
        return Response({
            'message': 'Perfil creado/actualizado exitosamente',
            'profile': ProfileSerializer(request.user, context={'request': request}).data,
        }, status=status.HTTP_201_CREATED)


class PublicProfileView(generics.RetrieveAPIView):
    """
    Vista para obtener perfiles 'públicos'. Dado que tu modelo no tiene is_public,
    usamos is_active=True como criterio básico (ajústalo si tu lógica de “público” es otra).
    """

    serializer_class = PublicProfileSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(is_active=True)
    lookup_url_kwarg = 'username'  # ajusta si tu URL usa otro kwarg

    def get_object(self):
        """Retorna el usuario por username"""
        username = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(
            self.get_queryset(),
            username=username,
        )


class ProfileSettingsView(generics.UpdateAPIView):
    """
    Vista para actualizar configuraciones del 'perfil' del usuario.
    Operamos directamente sobre request.user.
    """

    serializer_class = ProfileSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Configuraciones del perfil actualizadas exitosamente',
            'settings': ProfileSettingsSerializer(instance).data,
        })


class ProfileCompletionView(APIView):
    """
    Vista para obtener el porcentaje de completitud del perfil.
    Trabajamos con el CustomUser directamente.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Si tienes métodos en el modelo (get_completion_percentage / is_complete),
        # puedes usarlos. Si no, calculamos algo básico aquí.
        if hasattr(user, 'get_completion_percentage'):
            completion_percentage = user.get_completion_percentage()
            is_complete = user.is_complete() if hasattr(user, 'is_complete') else completion_percentage == 100
        else:
            # Cálculo simple basado en campos disponibles
            required_fields = [
                'first_name',
                'paternal_lastname',
                'sex',          # en tu modelo existe 'sex' (no 'gender')
                'email',
            ]
            filled = sum(bool(getattr(user, f, None)) for f in required_fields)
            completion_percentage = int((filled / len(required_fields)) * 100)
            is_complete = completion_percentage == 100

        return Response({
            'completion_percentage': completion_percentage,
            'is_complete': is_complete,
            'missing_fields': self._get_missing_fields(user),
        })

    def _get_missing_fields(self, user):
        """Retorna los campos que faltan para completar el perfil (según tu modelo real)."""
        missing = []

        if not getattr(user, 'first_name', None):
            missing.append('first_name')
        if not getattr(user, 'paternal_lastname', None):
            missing.append('paternal_lastname')
        if not getattr(user, 'sex', None):
            missing.append('sex')
        if not getattr(user, 'email', None):
            missing.append('email')

        # Foto de perfil: tu modelo tiene 'photo_url'
        if not getattr(user, 'photo_url', None):
            missing.append('photo_url')

        return missing


class ProfileSearchView(generics.ListAPIView):
    """
    Vista para buscar 'perfiles' públicos.
    Sin 'is_public', usamos is_active=True como filtro base.
    """

    serializer_class = PublicProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filtra usuarios según parámetros de búsqueda"""
        queryset = User.objects.filter(is_active=True)

        # Búsqueda por nombre
        name_query = self.request.query_params.get('name')
        if name_query:
            queryset = queryset.filter(
                models.Q(first_name__icontains=name_query) |
                models.Q(paternal_lastname__icontains=name_query) |
                models.Q(maternal_lastname__icontains=name_query) |
                models.Q(username__icontains=name_query) |
                models.Q(email__icontains=name_query)
            )

        # Filtro por sexo (tu modelo usa 'sex')
        sex = self.request.query_params.get('gender') or self.request.query_params.get('sex')
        if sex:
            queryset = queryset.filter(sex=sex)

        # Si tu modelo tuviera país/ciudad los agregaríamos aquí. En tu traceback no aparecen.

        return queryset.select_related().order_by('-updated_at')[:50]  # Limitar a 50 resultados
