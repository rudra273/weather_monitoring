import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from .models import WeatherData, DailySummary, AlertConfig, Alert
from collections import Counter

@shared_task
def fetch_weather_data():
    for city in settings.CITIES:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.OPENWEATHERMAP_API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            WeatherData.objects.create(
                city=city,
                main=data['weather'][0]['main'],
                temp=data['main']['temp'] - 273.15,  # Convert to Celsius
                feels_like=data['main']['feels_like'] - 273.15,  # Convert to Celsius
                timestamp=timezone.now()
            )
            check_alerts(city)

@shared_task
def generate_daily_summary():
    today = timezone.now().date()
    for city in settings.CITIES:
        data = WeatherData.objects.filter(city=city, timestamp__date=today)
        if data:
            temps = [d.temp for d in data]
            conditions = [d.main for d in data]
            DailySummary.objects.update_or_create(
                city=city,
                date=today,
                defaults={
                    'avg_temp': sum(temps) / len(temps),
                    'max_temp': max(temps),
                    'min_temp': min(temps),
                    'dominant_condition': Counter(conditions).most_common(1)[0][0]
                }
            )

def check_alerts(city):
    latest_data = WeatherData.objects.filter(city=city).order_by('-timestamp').first()
    if latest_data:
        config = AlertConfig.objects.filter(city=city).first()
        if config:
            if latest_data.temp > config.max_temp:
                Alert.objects.create(city=city, message=f"High temperature alert: {latest_data.temp}°C")
            elif latest_data.temp < config.min_temp:
                Alert.objects.create(city=city, message=f"Low temperature alert: {latest_data.temp}°C")
            elif config.condition and latest_data.main == config.condition:
                Alert.objects.create(city=city, message=f"Weather condition alert: {latest_data.main}")