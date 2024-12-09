# AmbulanceAlertingSystem/urls.py

from django.contrib import admin
from django.urls import path
from main_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('admin-page/', views.admin_page, name='admin-page'),
    path('hospital/', views.hospital_view, name='hospital'),
    path('traffic-police/', views.traffic_police_view, name='traffic_police'),
    path('ambulance-drive/', views.ambulance_drive, name='ambulance_drive'),
    path('api/hospital/', views.get_hospital_by_name, name='get_hospital_by_name'),
    path('api/signal/', views.get_signal_by_name, name='get_signal_by_name'),
]
