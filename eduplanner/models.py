# Este modelo utilizará el ORM de Django para interactuar con la base de datos.
# Calendar/models.py
from django.db import models

class EventoAcademico(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.titulo
