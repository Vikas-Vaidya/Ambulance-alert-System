# AmbulanceAlertingSystem/urls.py

from django.contrib import admin
from django.urls import path
from main_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('admin-page/', views.admin, name='admin'),
    path('hospital/', views.hospital_view, name='hospital'),
    path('traffic-police/', views.traffic_police_view, name='traffic_police'),
    path('ambulance-drive/', views.ambulance_drive, name='ambulance_drive'),
]
