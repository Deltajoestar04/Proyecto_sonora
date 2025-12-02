from django.db import models


class SensorData(models.Model):
    """Modelo para datos históricos del sensor."""

    topic = models.CharField(max_length=255)
    municipio = models.CharField(max_length=100)
    tipo_dato = models.CharField(max_length=50)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.topic}: {self.value}"

    class Meta:
        ordering = ['-timestamp']
