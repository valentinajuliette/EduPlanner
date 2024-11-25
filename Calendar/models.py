from django.db import models

class EventosAcademicos(models.Model):
    LISTA_TIPOS = {
        "1": "Inicio de Semestre",
        "2": "Fin de Semestre",
        "3": "Inicio de Inscripción de Asignaturas",
        "4": "Fin de Inscripción de Asignaturas",
        "5": "Receso Académico",
        "6": "Feriado Nacional", # Default 4 Feriados
        "7": "Feriado Regional",
        "8": "Inicio de Plazos de Solicitudes Administrativas",
        "9": "Fin de Plazos de Solicitudes Administrativas",
        "10": "Inicio de Plazos para la Gestión de Beneficios",
        "11": "Fin de Plazos para la Gestión de Beneficios",
        "12": "Ceremonia de Titulación o Graduación",
        "13": "Reunión de Consejo Académico",
        "14": "Talleres y Charlas",
        "15": "Día de Orientación para Nuevos Estudiantes",
        "16": "Eventos Extracurriculares",
        "17": "Inicio de Clases",
        "18": "Último Día de Clases",
        "19": "Día de Puertas Abiertas",
        "20": "Suspensión de Actividades Completa",
        "21": "Suspensión de Actividades Parcial",
    }

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo = models.CharField(max_length=3, choices=LISTA_TIPOS.items())
    confidencial = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo