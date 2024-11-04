from django.db import models

class User(models.Model):
    email_id = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=3)

    def __str__(self):
        return self.email_id

class TrafficSignal(models.Model):
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    s_s_status = models.BooleanField(default=True)  # 1 for Free, 0 for Busy
    discord_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Hospital(models.Model):
    h_discord_name = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=100)
    accept_patient = models.BooleanField(default=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.h_discord_name