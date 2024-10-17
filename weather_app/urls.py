from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('daily-summary/', views.daily_summary, name='daily_summary'),
]