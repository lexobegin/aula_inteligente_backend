#from django.shortcuts import render

# core/views.py
from rest_framework import viewsets, generics
from .models import Alumno, Profesor, Clase, Inscripcion, Nota, Asistencia, Participacion, PrediccionRendimiento
from .serializers import (AlumnoSerializer, RegistroUsuarioSerializer, ProfesorSerializer, ClaseSerializer, InscripcionSerializer, NotaSerializer, AsistenciaSerializer, ParticipacionSerializer, PrediccionRendimientoSerializer)

from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated

Usuario = get_user_model()

class RegistroUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroUsuarioSerializer
    permission_classes = [IsAuthenticated]

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    permission_classes = [IsAuthenticated]

class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    permission_classes = [IsAuthenticated]

class ClaseViewSet(viewsets.ModelViewSet):
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer
    permission_classes = [IsAuthenticated]

class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated]

class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer
    permission_classes = [IsAuthenticated]

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
    permission_classes = [IsAuthenticated]

class ParticipacionViewSet(viewsets.ModelViewSet):
    queryset = Participacion.objects.all()
    serializer_class = ParticipacionSerializer
    permission_classes = [IsAuthenticated]

class PrediccionViewSet(viewsets.ModelViewSet):
    queryset = PrediccionRendimiento.objects.all()
    serializer_class = PrediccionRendimientoSerializer
    permission_classes = [IsAuthenticated]
