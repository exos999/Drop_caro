from django.db import models
from django.contrib.auth.models import User


class DriverDetails(models.Model):
    fullname = models.CharField(max_length=150, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    license_number = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='driver_photos/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True,null=True)

   
    
class UserDetails(models.Model):
    fullname = models.CharField(max_length=150, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address_line1 = models.TextField(null=True, blank=True)
    
    
class VehicleRegistration(models.Model):
    vehicle_number = models.CharField(max_length=20, unique=True,blank=True, null=True)
    owner = models.ForeignKey(UserDetails, on_delete=models.CASCADE, blank=True, null=True)
    vehicle_model = models.CharField(max_length=100,blank=True, null=True)
    contact = models.CharField(max_length=15,blank=True, null=True)


class MaintenanceRequest(models.Model):
    full_name = models.CharField(max_length=100)
    vehicle = models.ForeignKey(VehicleRegistration, on_delete=models.CASCADE,null=True,blank=True)
    services = models.TextField()  
    description = models.TextField(blank=True, null=True)
    request_date = models.DateField()
    request_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class DriverBooking(models.Model):
    full_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    key_point = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)