# Se crea un modelo que represente los perritos del refugio.
# Este modelo utilizará el ORM de Django para interactuar con la base de datos.

from django.db import models

class EventoAcademico(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.titulo