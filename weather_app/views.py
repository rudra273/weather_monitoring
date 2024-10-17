from django.shortcuts import render
from django.utils import timezone
from .models import WeatherData, DailySummary, Alert
import matplotlib.pyplot as plt
import io
import base64

def index(request):
    cities = WeatherData.objects.values('city').distinct()
    latest_data = {}
    for city in cities:
        latest_data[city['city']] = WeatherData.objects.filter(city=city['city']).order_by('-timestamp').first()
    
    alerts = Alert.objects.order_by('-timestamp')[:10]
    
    context = {
        'latest_data': latest_data,
        'alerts': alerts,
    }
    return render(request, 'weather_app/index.html', context)

def daily_summary(request):
    city = request.GET.get('city', 'Delhi')
    summaries = DailySummary.objects.filter(city=city).order_by('-date')[:7]
    
    # Generate temperature trend chart
    dates = [s.date for s in summaries]
    avg_temps = [s.avg_temp for s in summaries]
    
    plt.figure(figsize=(10, 5))
    plt.plot(dates, avg_temps, marker='o')
    plt.title(f'Temperature Trend for {city}')
    plt.xlabel('Date')
    plt.ylabel('Average Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graph = base64.b64encode(image_png).decode('utf-8')
    
    context = {
        'summaries': summaries,
        'graph': graph,
        'city': city,
    }
    return render(request, 'weather_app/daily_summary.html', context)