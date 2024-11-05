# main_app/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, TrafficSignal, Hospital
import os
from dotenv import load_dotenv
from discordwebhook import Discord

load_dotenv()
disc = Discord(url=os.getenv('Trafic_webhook'))
disc2 = Discord(url=os.getenv('hospital_webhook'))

def home(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email_id=email, password=password)
            if user.profession == "hpt":
                return redirect("hospital")
            elif user.profession == "trp":
                return redirect("traffic_police")
            else:
                return redirect("ambulance_drive")
        except User.DoesNotExist:
            return render(request, 'index.html', {'password': "False"})
        
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        name = request.POST.get("name")
        profession = request.POST.get("profession")
        
        try:
            user, created = User.objects.get_or_create(email_id=email, password=password, name=name, profession=profession)
            if user.profession == "hpt":
                return redirect("hospital")
            elif user.profession == "trp":
                return redirect("traffic_police")
            else:
                return redirect("ambulance_drive")
        except User.DoesNotExist:
            return render(request, 'register.html', {'password': "False"})
        
    return render(request, 'register.html')



def admin(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("Email")
        profession = request.POST.get("profession")
        password = request.POST.get("password")

        User.objects.create(name=name, email_id=email, profession=profession, password=password)

        if profession == 'trp':
            location = request.POST.get("location")
            discord_name = request.POST.get("d_name")
            from1, to1 = request.POST.get("from1"), request.POST.get("to1")
            from2, to2 = request.POST.get("from2"), request.POST.get("to2")

            TrafficSignal.objects.create(from_location=from1, to_location=to1, location=location, name=name, s_s_status=True, discord_name=discord_name)
            if from2 and to2:
                TrafficSignal.objects.create(from_location=from2, to_location=to2, location=location, name=name, s_s_status=True, discord_name=discord_name)

        elif profession == "hpt":
            hospital_name = request.POST.get("hospital")
            accept_patient = int(request.POST.get("attendpatient"))
            discord_name_d = request.POST.get("d_name-d")
            hpt_location = request.POST.get("hospitallocation")

            Hospital.objects.create(h_discord_name=discord_name_d, hospital_name=hospital_name, accept_patient=accept_patient, location=hpt_location)

        return HttpResponse("<h1>Record added Successfully</h1>")

    return render(request, 'Admin-Page.html')

def hospital_view(request):
    hospitals = Hospital.objects.all()
    if request.method == 'POST':
        hospital_name = request.POST.get('hospital_name_hp')
        accept_patient = request.POST.get('accept_patient')
        
        hospital = Hospital.objects.get(hospital_name=hospital_name)
        hospital.accept_patient = bool(int(accept_patient))
        hospital.save()

        return render(request, 'hospital.html', {'hospital_name_hp': hospitals, 'record_updated': "Changed successfully"})

    return render(request, 'hospital.html', {'hospital_name_hp': hospitals})

def traffic_police_view(request):
    traffic_signals = TrafficSignal.objects.values('location', 's_s_status').distinct()
    if request.method == 'POST':
        traffic_location = request.POST.get('traffic_name_tp')
        signal_status = bool(int(request.POST.get('Signal_Status')))

        TrafficSignal.objects.filter(location=traffic_location).update(s_s_status=signal_status)

        return render(request, 'traffic_police.html', {'traffic_list': traffic_signals, 'record_updated': "Changed successfully"})

    return render(request, 'traffic_police.html', {'traffic_list': traffic_signals})

def ambulance_drive(request):
    from_list = TrafficSignal.objects.values('from_location', 'to_location')

    if request.method == "POST":
        route_from = request.POST.get("ambulancedriver-from")
        route_to = request.POST.get("ambulancedriver-to")
        
        signal_details = TrafficSignal.objects.filter(from_location=route_from, to_location=route_to)
        hospital_details = Hospital.objects.filter(location=route_to)
        
        text_hospital_name = ', '.join([h.hospital_name for h in hospital_details])
        disc2.post(content=f"A patient is coming to {route_to}. Your hospital {text_hospital_name} covers this location, get ready with the bed")

        for signal in signal_details:
            status = "Free" if signal.s_s_status else "Busy"
            disc.post(content=f"Ambulance is coming in {signal.location}, {signal.name}. free the road from {route_from} to {route_to}")

        return render(request, 'Ambulance_driver_Page.html', {'signal_details': signal_details, 'fromlist': from_list, 'hospital_details': hospital_details})

    return render(request, 'Ambulance_driver_Page.html', {'fromlist': from_list})
