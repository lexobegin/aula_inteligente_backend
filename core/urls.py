# core/urls.py
from rest_framework import routers
from django.urls import path, include
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'alumnos', AlumnoViewSet)
router.register(r'profesores', ProfesorViewSet)
router.register(r'clases', ClaseViewSet)
router.register(r'inscripciones', InscripcionViewSet)
router.register(r'notas', NotaViewSet)
router.register(r'asistencias', AsistenciaViewSet)
router.register(r'participaciones', ParticipacionViewSet)
router.register(r'predicciones', PrediccionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # JWT login (obtener token)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Refrescar token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistroUsuarioView.as_view(), name='registro_usuario'),
]
