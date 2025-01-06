from django import forms
from .models import DriverDetails,UserDetails,VehicleRegistration,MaintenanceRequest,DriverBooking


class DriverDetailsForm(forms.ModelForm):
    class Meta:
        model = DriverDetails
        fields = ['fullname','email','password', 'phone', 'license_number', 'photo', 'date_of_birth']

# class DriverDetailsForm(forms.ModelForm):
#     class Meta:
#         model = DriverDetails
#         fields = ['username', 'email','password', 'phone', 'address_line1','license_number']

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['fullname','user', 'email', 'phone', 'address_line1']


class VehicleRegistrationForm(forms.ModelForm):
    class Meta:
        model = VehicleRegistration
        fields = ['vehicle_number', 'owner_name', 'vehicle_model', 'contact']


class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['full_name', 'vehicle_number', 'services', 'description', 'request_date', 'request_time']
        widgets = {
            'services': forms.CheckboxSelectMultiple(choices=[
                ('fuelRefill', 'Fuel Refill'),
                ('basicCheckup', 'Basic Checkup'),
                ('engineStart', 'Engine Start'),
                ('washing', 'Washing'),
            ]),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class DriverBookingForm(forms.ModelForm):
    class Meta:
        model = DriverBooking
        fields = ['full_name', 'contact_number', 'pickup_location', 'dropoff_location', 'pickup_date', 'pickup_time', 'key_point']
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'type': 'time'}),
        }
