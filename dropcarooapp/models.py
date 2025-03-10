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
    is_free = models.BooleanField(default=True)

    def __str__(self):
        return self.fullname
   
    
class UserDetails(models.Model):
    fullname = models.CharField(max_length=20, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)
    email = models.EmailField(unique=True)
    photo= models.ImageField(upload_to='user_photos/', blank=True, null=True)
    password = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    address_line1 = models.TextField(null=True, blank=True)
    
    
class VehicleRegistration(models.Model):
    vehicle_number = models.CharField(max_length=10, unique=True,blank=True, null=True)
    owner = models.ForeignKey(UserDetails, on_delete=models.CASCADE, blank=True, null=True)
    vehicle_model = models.CharField(max_length=10,blank=True, null=True)
    vehicle_address = models.CharField(max_length=255,blank=True, null=True)
    contact = models.CharField(max_length=10,blank=True, null=True)
    owner_name = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.vehicle_number


class MaintenanceRequest(models.Model):
    full_name = models.CharField(max_length=20,null=True,blank=True)
    contact = models.CharField(max_length=10, null=True, blank=True)  # Added this line
    vehicle = models.ForeignKey(VehicleRegistration, on_delete=models.CASCADE,null=True,blank=True)
    driver= models.ForeignKey(DriverDetails, on_delete=models.CASCADE,null=True,blank=True)
    services = models.TextField()
    address=models.CharField(max_length=255,blank=True, null=True)
    request_date = models.DateField(null=True,blank=True)
    request_time = models.TimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    

    

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
    vehicle= models.ForeignKey(VehicleRegistration, on_delete=models.CASCADE,null=True,blank=True)
    
from django.db import models

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('gpay', 'Google Pay'),
        ('paytm', 'Paytm'),
        ('phonepe', 'PhonePe'),
    ]
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, blank=True, null=True)  # Add this line
    driver = models.ForeignKey(DriverBooking, on_delete=models.CASCADE, blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    upi_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Track which form/page was used
    form_version = models.CharField(max_length=20, blank=True, null=True, choices=[
        ('standard', 'Standard Form'),
        ('premium', 'Premium Form')
    ])
    
    # Timestamp fields
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    # Status tracking
    payment_status = models.CharField(max_length=20, default='pending', blank=True, null=True)
    
    def __str__(self):
        return f"Payment: ₹{self.amount} via {self.get_payment_method_display()}"
    def save(self, *args, **kwargs):
        """
        Automatically assigns the driver from the DriverBooking model before saving.
        """
        if not self.driver and self.form_version:
            driver_booking = DriverBooking.objects.filter(user=self.user).last()  # Get latest booking for user
            if driver_booking and driver_booking.driver:
                self.driver = driver_booking.driver  # Assign driver
        
        super().save(*args, **kwargs)
    

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
    
    
class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('feedback', 'Feedback'),
        ('complaint', 'Complaint'),
    ]

    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES,null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.feedback_type}"
