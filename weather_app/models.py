from django.db import models

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    main = models.CharField(max_length=100)
    temp = models.FloatField()
    feels_like = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.city} - {self.timestamp}"

class DailySummary(models.Model):
    city = models.CharField(max_length=100)
    date = models.DateField()
    avg_temp = models.FloatField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    dominant_condition = models.CharField(max_length=100)

    class Meta:
        unique_together = ('city', 'date')

    def __str__(self):
        return f"{self.city} - {self.date}"

class AlertConfig(models.Model):
    city = models.CharField(max_length=100)
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    condition = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Alert Config for {self.city}"

class Alert(models.Model):
    city = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.timestamp}"