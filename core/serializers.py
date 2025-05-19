# core/serializers.py
from rest_framework import serializers
from .models import Usuario, Alumno, Profesor, Administrador, Apoderado, Materia, Clase, Inscripcion, Nota, Asistencia, Participacion, PrediccionRendimiento

from django.contrib.auth import get_user_model

Usuario = get_user_model()


# Usuario (para login, perfil, etc.)
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol', 'estado']

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'tipo_usuario']  # o los campos que usas

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user

# Alumno
class AlumnoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Alumno
        fields = '__all__'

# Profesor
class ProfesorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Profesor
        fields = '__all__'

# Clase
class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = '__all__'

# Inscripción
class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = '__all__'

# Nota
class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = '__all__'

# Asistencia
class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = '__all__'

# Participación
class ParticipacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participacion
        fields = '__all__'

# Predicción de rendimiento
class PrediccionRendimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrediccionRendimiento
        fields = '__all__'
