from django.shortcuts import render,redirect,get_object_or_404
from.models import*
from.form import UserDetailsForm,DriverDetailsForm,VehicleRegistrationForm,MaintenanceRequestForm,DriverBookingForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login


def home(request):
    return render(request,'dropcaro/home.html')


def ujk(request):
    return render(request,'dropcaro/ujk.html')


def about_view(request):
    return render(request,'dropcaro/about.html')


def service_view(request):
    return render(request,'dropcaro/service.html')

def contact_view(request):
    return render(request,'dropcaro/contact.html')

    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        
        if user is not None:
            login(request, user)
            # Redirect based on user group/role
            if UserDetails.objects.filter(user=user).exists():
                return redirect('user_dashboard')
            elif DriverDetails.objects.filter(user=user).exists():
                return redirect('driver_dashboard')
            else:
                return HttpResponse("Unauthorized role")
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request,'dropcaro/login.html')


def carowner_registration(request):
    if request.method == 'POST':
        data=request.POST.copy()
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        try:
            user=User.objects.create_user(username=username,password=password,email=email)
        except Exception as e:
            print(e)
            return redirect('carowner')
            
        
        user_form=UserDetailsForm(data)
        if user_form.is_valid():
            user_details=user_form.save(commit=False)  
            print(user)
            user_details.user=user
            user_details.save()
            messages.success(request, 'Registration successful!')  
            return redirect('login')  
        else:
            print(uesr_form.errors)
            messages.error(request, 'Please correct the errors below.') 
    else:
        user_form = UserDetailsForm() 
    return render(request,'dropcaro/carowner.html')



def driver_view(request):
    if request.method == 'POST':
        data=request.POST.copy()
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        try:
            user=User.objects.create_user(username=username,password=password,email=email)
        except Exception as e:
            print("e")
            return redirect('driver_reg')
        
        driver_form=DriverDetailsForm(data)
        if driver_form.is_valid():
            driver_details=driver_form.save(commit=False)
            print("driver") 
            driver_details.user=user
            driver_form.save()  
            messages.success(request, 'Registration successful!')  
            return redirect('login')  
        else:
            print(driver_form.errors)
            messages.error(request, 'Please correct the errors below.') 
    else:
        uesr_form = DriverDetailsForm() 
    return render(request,'dropcaro/driver_reg.html')



def cupass_view(request):
    return render(request,'dropcaro/cus_password.html')

def drvpass_view(request):
    return render(request,'dropcaro/driver_password.html')

def book_driver_view(request):
    return render(request,'dropcaro/bookdriver.html')

def book_maintance_view(request):
    return render(request,'dropcaro/bookmaintance.html')

def user_dashboard_view(request):
    return render(request,'dropcaro/user_dashboard.html')

def driver_dashboard_view(request):
    return render(request,'dropcaro/driver_dashboard.html')


def admin_dashboard_view(request):
    return render(request,'dropcaro/admin_dashboard.html')



# user_dashboard_view
from django.shortcuts import render

# def  home(request):
#     return render(request, 'home.html')

# def my_vehicles(request):
#     return render(request, 'vehicles.html')



def track_vehicle(request):
    return render(request, 'track.html')

# def maintenance_reg(request):
#     return render(request, 'dropcaro/maintenance_reg.html')

def payments(request):
    return render(request, 'payments.html')

def logout_view(request):
    # Add logic for logging out the user
    return render(request, 'logout.html')

# vehicle reg url
# views.py

from django.shortcuts import render

# Create your views here.
def map(request):
    context = {
        'latitude': 11.2588,
        'longitude': 75.7804
    }
    return render(request, 'map.html', context)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt 
def save_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        print(f"Received coordinates: Latitude={latitude}, Longitude={longitude}")

        return JsonResponse({'status': 'success', 'latitude': latitude, 'longitude': longitude})
    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)
# def vehicle_reg(request):
#     if request.method == "POST":
#         data=request.POST.copy()
#         vehicle_number = request.POST.get('vehicle_number')
#         owner_name = request.POST.get('owner_name')
#         vehicle_model = request.POST.get('vehicle_model')
#         contact = request.POST.get('contact')

#         try:
#             user=Vehicle.objects.create(
#                 vehicle_number=vehicle_number,
#                 owner_name=owner_name,
#                 vehicle_model=vehicle_model,
#                 contact=contact
#             )
#             messages.success(request, "Vehicle registered successfully!")
#         except Exception as e:
#             print("e")
#             messages.error(request, f"Error: {str(e)}")

#         return redirect('vehicle_reg')
    
#     return render(request, 'dropcaro/vehicle_reg.html')


# VehicleRegistration view
def vehicle_reg(request):
    if request.method == "POST":
        form = VehicleRegistrationForm(request.POST)
        if form.is_valid():
            userds=get_object_or_404(UserDetails,user=request.user)
            vehicle=form.save(commit=False)
            vehicle.owner=userds
            vehicle.save()
            messages.success(request, "Vehicle registered successfully!")
            return redirect('user_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = VehicleRegistrationForm()

    return render(request, 'dropcaro/vehicle_reg.html', {'form': form})


# MaintenanceRequest view

def maintenance_reg(request):
    if request.method == "POST":
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            vehicle_id=request.POST.get('vehicle')
            maintenance_request = form.save(commit=False)
            # Combine selected services into a comma-separated string
            services = request.POST.getlist('services')
            maintenance_request.services = ','.join(services)
            vehicle=get_object_or_404(VehicleRegistration,id=vehicle_id)
            maintenance_request.vehicle=vehicle
            maintenance_request.save()
            messages.success(request, "Your maintenance request has been submitted successfully!")
            return redirect('user_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = MaintenanceRequestForm()

    vehicles=VehicleRegistration.objects.filter(owner__user=request.user)
    return render(request, 'dropcaro/maintenance_reg.html', {'form': form,'vehicles':vehicles})

def admin_list_maintenance(request):
    maintenance_bookings = MaintenanceRequest.objects.all() 
    return render(request, 'dropcaro/admin_list_maintenance.html', {'maintenance_bookings': maintenance_bookings})

# book_driver
def book_driver(request):
    if request.method == "POST":
        form = DriverBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Driver booked successfully!")
            return redirect('user_dashboard')  # Redirect to prevent form resubmission
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = DriverBookingForm()

    return render(request, 'dropcaro/book_driver.html', {'form': form})


# driver_dashboard_view
# view task

def view_task(request):
    return render(request, 'dropcaro/view_task.html')


# admin_dashboard_view

def manage_users(request):
    users=UserDetails.objects.all()
    return render(request, 'dropcaro/manage_users.html',{"users":users})

def manage_drivers(request):
    drivers=DriverDetails.objects.all()
    
    return render(request, 'dropcaro/manage_drivers.html',{"drivers":drivers})


def vehicle_details(request):
    vehicles=VehicleRegistration.objects.all()
    
    return render(request, 'dropcaro/vehicle_details.html',{"vehicles":vehicles})


def view_bookdriver(request):
    bookdriver=DriverBooking.objects.all()
    
    return render(request, 'admin_dashboard/view_bookdriver.html',{"bookdriver":bookdriver})


def view_bookmaintance(request):
    bookmaintance=MaintenanceRequest.objects.all()
    
    return render(request, 'admin_dashboard/view_bookmaintance.html',{"bookmaintance":bookmaintance})

# payment


def payment(request):
    return render(request, 'payment/payment.html')

def sucessfull_payment(request):
    return render(request, 'payment/sucessfull_payment.html')