from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Usuario(AbstractUser):
    estado = models.CharField(max_length=20, default='ACTIVO')

    ROL_CHOICES = [
        ('ADMINISTRADOR', 'Administrador'),
        ('PROFESOR', 'Profesor'),
        ('ALUMNO', 'Alumno'),
        ('APODERADO', 'Apoderado'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"
    
class Administrador(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, null=True, blank=True)

class Profesor(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)
    especialidad = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    fecha_contratacion = models.DateField()

class Alumno(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    direccion = models.TextField()
    telefono_emergencia = models.CharField(max_length=40, null=True, blank=True)

class Apoderado(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)
    parentesco = models.CharField(max_length=50)
    ocupacion = models.CharField(max_length=100)
    direccion_trabajo = models.TextField()
    telefono = models.CharField(max_length=20)

class AlumnoApoderado(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE)
    parentesco = models.CharField(max_length=50)
    es_principal = models.BooleanField(default=False)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['alumno', 'apoderado'], name='unique_alumno_apoderado')
    ]

class GestionAcademica(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, default='PLANIFICADA')

    def __str__(self):
        return self.nombre

class PeriodoAcademico(models.Model):
    gestion = models.ForeignKey(GestionAcademica, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    creditos = models.IntegerField()
    nivel = models.CharField(max_length=50)

class Aula(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    edificio = models.CharField(max_length=50)
    piso = models.IntegerField()
    capacidad = models.IntegerField()
    tipo = models.CharField(max_length=50)
    equipamiento = models.TextField(blank=True)

class Clase(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    periodo = models.ForeignKey(PeriodoAcademico, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    horario = models.CharField(max_length=100)

class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='ACTIVA')

class Nota(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    periodo = models.ForeignKey(PeriodoAcademico, on_delete=models.CASCADE)
    tipo_evaluacion = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_registro = models.DateField(auto_now_add=True)

class Asistencia(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=20)  # 'PRESENTE', 'AUSENTE', etc.
    justificacion = models.TextField(blank=True, null=True)

class Participacion(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    fecha = models.DateField()
    tipo = models.CharField(max_length=50)  # 'ORAL', 'PROYECTO', etc.
    valoracion = models.IntegerField()
    comentarios = models.TextField(blank=True)

class PrediccionRendimiento(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    fecha_prediccion = models.DateTimeField(auto_now_add=True)
    valor_prediccion = models.DecimalField(max_digits=5, decimal_places=2)
    categoria_rendimiento = models.CharField(max_length=20)  # 'BAJO', 'MEDIO', 'ALTO'
    modelo_utilizado = models.CharField(max_length=100)
