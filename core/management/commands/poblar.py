# core/management/commands/poblar.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Alumno, Profesor, Apoderado, Nota, PrediccionRendimiento, GestionAcademica, PeriodoAcademico, Materia, Aula, Clase, Inscripcion
from faker import Faker
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de prueba'

    def handle(self, *args, **kwargs):
        fake = Faker()
        Usuario = get_user_model()

        self.stdout.write("Creando usuarios...")

        # Crear admin si no existe
        admin = Usuario.objects.filter(username='admin').first()
        if not admin:
            admin = Usuario(username='admin', email='admin@test.com', rol='ADMINISTRADOR')
            admin.set_password('admin123')
            admin.save()
            self.stdout.write("Admin creado.")
        else:
            self.stdout.write("Admin ya existe.")

        alumnos = []
        for i in range(5):
            username = f'alumno{i}'
            user = Usuario.objects.filter(username=username).first()
            if not user:
                user = Usuario(
                    username=username,
                    email=f'{username}@test.com',
                    rol='ALUMNO'
                )
                user.set_password('12345678')
                user.save()
                alumno = Alumno.objects.create(
                    usuario=user,
                    fecha_nacimiento=fake.date_of_birth(minimum_age=10, maximum_age=20),
                    genero=random.choice(['M', 'F']),
                    direccion=fake.address(),
                    telefono_emergencia=fake.phone_number()
                )
                alumnos.append(alumno)
                self.stdout.write(f"Alumno creado: {username}")
            else:
                self.stdout.write(f"Usuario {username} ya existe, omitiendo.")

        profesores = []
        for i in range(3):
            username = f'profesor{i}'
            user = Usuario.objects.filter(username=username).first()
            if not user:
                user = Usuario(
                    username=username,
                    email=f'{username}@test.com',
                    rol='PROFESOR'
                )
                user.set_password('12345678')
                user.save()
                profesor = Profesor.objects.create(
                    usuario=user,
                    especialidad=fake.job(),
                    titulo=fake.job(),
                    fecha_contratacion=fake.date_between(start_date='-10y', end_date='today')
                )
                profesores.append(profesor)
                self.stdout.write(f"Profesor creado: {username}")
            else:
                self.stdout.write(f"Usuario {username} ya existe, omitiendo.")

        apoderados = []
        for i in range(2):
            username = f'apoderado{i}'
            user = Usuario.objects.filter(username=username).first()
            if not user:
                user = Usuario(
                    username=username,
                    email=f'{username}@test.com',
                    rol='APODERADO'
                )
                user.set_password('12345678')
                user.save()
                apoderado = Apoderado.objects.create(
                    usuario=user,
                    parentesco='Padre',
                    ocupacion=fake.job(),
                    direccion_trabajo=fake.address(),
                    telefono=fake.phone_number()
                )
                apoderados.append(apoderado)
                self.stdout.write(f"Apoderado creado: {username}")
            else:
                self.stdout.write(f"Usuario {username} ya existe, omitiendo.")

        # Crear una gestión académica y periodo
        gestion, _ = GestionAcademica.objects.get_or_create(
            nombre='Gestión 2025',
            defaults={'fecha_inicio': date.today(), 'fecha_fin': date.today() + timedelta(days=120), 'estado': 'EN CURSO'}
        )
        periodo, _ = PeriodoAcademico.objects.get_or_create(
            gestion=gestion,
            nombre='Primer Trimestre',
            defaults={'fecha_inicio': gestion.fecha_inicio, 'fecha_fin': gestion.fecha_fin, 'tipo': 'Trimestral'}
        )

        # Crear materia, aula, clase
        materia, _ = Materia.objects.get_or_create(
            nombre='Matemáticas',
            defaults={'descripcion': 'Curso de matemáticas', 'creditos': 4, 'nivel': 'Básico'}
        )
        aula, _ = Aula.objects.get_or_create(
            codigo='A-101',
            defaults={'edificio': 'Principal', 'piso': 1, 'capacidad': 30, 'tipo': 'Teoría', 'equipamiento': 'Pizarra, proyector'}
        )
        clase, _ = Clase.objects.get_or_create(
            materia=materia,
            profesor=profesores[0],
            periodo=periodo,
            aula=aula,
            defaults={'horario': 'Lunes y Miércoles 08:00 - 10:00'}
        )

        self.stdout.write("Clases creadas correctamente.")

        self.stdout.write("Creando inscripciones, notas y predicciones...")
        for alumno in alumnos:
            inscripcion, _ = Inscripcion.objects.get_or_create(
                alumno=alumno,
                clase=clase
            )

            # Crear notas
            for tipo_eval in ['Parcial', 'Final']:
                Nota.objects.get_or_create(
                    inscripcion=inscripcion,
                    periodo=periodo,
                    tipo_evaluacion=tipo_eval,
                    defaults={'valor': round(random.uniform(4.0, 10.0), 2)}
                )

            # Crear predicción
            PrediccionRendimiento.objects.get_or_create(
                inscripcion=inscripcion,
                defaults={
                    'valor_prediccion': round(random.uniform(0.0, 10.0), 2),
                    'categoria_rendimiento': random.choice(['BAJO', 'MEDIO', 'ALTO']),
                    'modelo_utilizado': 'ModeloDummyV1'
                }
            )

        self.stdout.write("Datos académicos creados correctamente.")
