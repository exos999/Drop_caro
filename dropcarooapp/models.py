from django.db import models
from django.contrib.auth.models import User


class DriverDetails(models.Model):
    fullname = models.CharField(max_length=20, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    license_number = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='driver_photos/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True,null=True)
    city = models.CharField(max_length=15,blank=True,null=True)

   
    
class UserDetails(models.Model):
    fullname = models.CharField(max_length=20, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    address_line1 = models.TextField(null=True, blank=True)
    
    
class VehicleRegistration(models.Model):
    vehicle_number = models.CharField(max_length=10, unique=True,blank=True, null=True)
    owner = models.ForeignKey(UserDetails, on_delete=models.CASCADE, blank=True, null=True)
    vehicle_model = models.CharField(max_length=10,blank=True, null=True)
    contact = models.CharField(max_length=10,blank=True, null=True)
    owner_name = models.CharField(max_length=100,blank=True, null=True)


class MaintenanceRequest(models.Model):
    full_name = models.CharField(max_length=20)
    vehicle = models.ForeignKey(VehicleRegistration, on_delete=models.CASCADE,null=True,blank=True)
    driver= models.ForeignKey(DriverDetails, on_delete=models.CASCADE,null=True,blank=True)
    services = models.TextField()  
    description = models.TextField(blank=True, null=True)
    request_date = models.DateField()
    request_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class DriverBooking(models.Model):
    full_name = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=10)
    pickup_location = models.CharField(max_length=20)
    dropoff_location = models.CharField(max_length=20)
    driver= models.ForeignKey(DriverDetails, on_delete=models.CASCADE,null=True,blank=True)
    user= models.ForeignKey(UserDetails, on_delete=models.CASCADE,null=True,blank=True)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    key_point = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('gpay', 'Google Pay'),
        ('paytm', 'Paytm'),
        ('phonepe', 'PhonePe'),
    ]

    user=models.ForeignKey(UserDetails,on_delete=models.CASCADE,null=True,blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    upi_id = models.CharField(max_length=100,null=True,blank=True)
    createdat= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_method} - {self.amount}"
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True ,related_name='notification_customer')
    title = models.CharField(max_length=100,null=True,blank=True)
    # type = models.CharField(max_length=20,null=True,blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.title if self.title else 'Notification'
    


class Location(models.Model):
    latitude = models.FloatField(null=True,blank=True)
    task = models.ForeignKey('DriverBooking', on_delete=models.CASCADE,null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Location of {self.task.driver.user.username} at {self.timestamp}"
