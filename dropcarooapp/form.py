from django import forms
from .models import DriverDetails,UserDetails,VehicleRegistration,MaintenanceRequest,DriverBooking,Payment


class DriverDetailsForm(forms.ModelForm):
    class Meta:
        model = DriverDetails
        fields = ['fullname','email','password', 'phone', 'license_number', 'photo', 'date_of_birth','city']

# class DriverDetailsForm(forms.ModelForm):
#     class Meta:
#         model = DriverDetails
#         fields = ['username', 'email','password', 'phone', 'address_line1','license_number']

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['fullname','user', 'email','photo', 'phone', 'address_line1']


class VehicleRegistrationForm(forms.ModelForm):
    class Meta:
        model = VehicleRegistration
        fields = ['vehicle_number', 'vehicle_model', 'vehicle_address','contact','owner_name']



class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['full_name','contact', 'vehicle', 'services',  'address', 'request_date', 'request_time']
        widgets = {
            'services': forms.CheckboxSelectMultiple(choices=[
                ('fuelRefill', 'Fuel Refill'),
                ('basicCheckup', 'Basic Checkup'),
                ('engineStart', 'Engine Start'),
                ('washing', 'Washing'),
            ]),
            'address': forms.Textarea(attrs={'rows': 4}),
        }



class DriverBookingForm(forms.ModelForm):
    class Meta:
        model = DriverBooking
        fields = ['full_name', 'contact_number', 'pickup_location', 'dropoff_location', 'pickup_date', 'pickup_time', 'key_point']
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'type': 'time'}),
        }


from django import forms
from .models import Payment

class StandardPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'amount', 'upi_id']
        widgets = {
            'amount': forms.NumberInput(attrs={'readonly': True, 'step': '0.01', 'value': '499'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Basic styling for standard form
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Add a hidden field for form version
        self.initial['form_version'] = 'standard'

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.form_version = 'standard'
        if commit:
            instance.save()
        return instance


class PremiumPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'amount', 'upi_id']
        widgets = {
            'amount': forms.NumberInput(attrs={'readonly': True, 'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Premium styling with enhanced attributes
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Add specific attributes for the premium form
        self.fields['upi_id'].widget.attrs.update({'placeholder': 'example@upi'})
        
        # Add a hidden field for form version
        self.initial['form_version'] = 'premium'
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.form_version = 'premium'
        if commit:
            instance.save()
        return instance