from django.db import models

class Lectura(models.Model):
    municipio = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    valor = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.municipio} - {self.tipo}: {self.valor}"
