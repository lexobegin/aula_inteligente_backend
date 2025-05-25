#from django.shortcuts import render

# core/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model

from .models import *
from .serializers import *

from core.utils.ml.ml_model import predecir_rendimiento

Usuario = get_user_model()

# Usuario actual //me
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usuario_actual(request):
    usuario = request.user
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)

# Registro
class RegistroUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroUsuarioSerializer
    permission_classes = [IsAuthenticated]

# Usuarios relacionados
class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    permission_classes = [IsAuthenticated]

class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    permission_classes = [IsAuthenticated]

class ApoderadoViewSet(viewsets.ModelViewSet):
    queryset = Apoderado.objects.all()
    serializer_class = ApoderadoSerializer
    permission_classes = [IsAuthenticated]

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    permission_classes = [IsAuthenticated]

# Relaciones
class AlumnoApoderadoViewSet(viewsets.ModelViewSet):
    queryset = AlumnoApoderado.objects.all()
    serializer_class = AlumnoApoderadoSerializer
    permission_classes = [IsAuthenticated]

# Gestión académica
class GestionViewSet(viewsets.ModelViewSet):
    queryset = Gestion.objects.all()
    serializer_class = GestionSerializer
    permission_classes = [IsAuthenticated]

class PeriodoViewSet(viewsets.ModelViewSet):
    queryset = Periodo.objects.all()
    serializer_class = PeriodoSerializer
    permission_classes = [IsAuthenticated]

class GestionPeriodoViewSet(viewsets.ModelViewSet):
    queryset = GestionPeriodo.objects.all()
    serializer_class = GestionPeriodoSerializer
    permission_classes = [IsAuthenticated]

class GradoViewSet(viewsets.ModelViewSet):
    queryset = Grado.objects.all()
    serializer_class = GradoSerializer
    permission_classes = [IsAuthenticated]

class GestionGradoViewSet(viewsets.ModelViewSet):
    queryset = GestionGrado.objects.all()
    serializer_class = GestionGradoSerializer
    permission_classes = [IsAuthenticated]

class GestionGradoMateriaViewSet(viewsets.ModelViewSet):
    queryset = GestionGradoMateria.objects.all()
    serializer_class = GestionGradoMateriaSerializer
    permission_classes = [IsAuthenticated]

# Academico
class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer
    permission_classes = [IsAuthenticated]

class AulaViewSet(viewsets.ModelViewSet):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer
    permission_classes = [IsAuthenticated]

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    permission_classes = [IsAuthenticated]

class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated]

# Evaluaciones
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

class PrediccionRendimientoAPIView(APIView):
    def post(self, request):
        data = request.data

        try:
            promedio_notas = float(data.get("promedio_notas"))
            asistencia = float(data.get("asistencia"))
            participacion = float(data.get("participacion"))
        except (TypeError, ValueError):
            return Response({"error": "Datos inválidos."}, status=status.HTTP_400_BAD_REQUEST)

        prediccion, clasificacion = predecir_rendimiento(promedio_notas, asistencia, participacion)

        return Response({
            "prediccion": round(prediccion, 2),
            "clasificacion": clasificacion
        }, status=status.HTTP_200_OK)
