from django.shortcuts import render,redirect,get_object_or_404
from.models import*
from.form import UserDetailsForm,DriverDetailsForm,VehicleRegistrationForm,MaintenanceRequestForm,DriverBookingForm,PaymentForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
# from .models import VehicleRegistration
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Location, DriverDetails, DriverBooking,Feedback


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


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
            elif user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return HttpResponse("Unauthorized role")
        else:
            return render(request, 'dropcaro/login.html', {'error': 'Invalid credentials'})

    return render(request,'dropcaro/login.html')



def carowner_registration(request):
    if request.method == 'POST':
        data = request.POST.copy()
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except Exception as e:
            print(e)
            messages.error(request, 'Error creating user: {}'.format(str(e)))
            return redirect('carowner')
        
        user_form = UserDetailsForm(data)
        if user_form.is_valid():
            user_details = user_form.save(commit=False)
            user_details.user = user
            user_details.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
        else:
            print(user_form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserDetailsForm()

    return render(request, 'dropcaro/carowner.html', {'form': user_form})



def driver_view(request):
    if request.method == 'POST':
        data=request.POST.copy()
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        try:
            user=User.objects.create_user(username=username,password=password,email=email)
        except Exception as e:
            print(e)
            return redirect('driver_reg')
        
        driver_form=DriverDetailsForm(data,request.FILES)
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


def book_driver_view(request):
    return render(request,'dropcaro/bookdriver.html')

def book_maintance_view(request):
    return render(request,'dropcaro/bookmaintance.html')

@login_required
def user_dashboard_view(request):
    return render(request,'dropcaro/user_dashboard.html')

@login_required
def driver_dashboard_view(request):
    driver=request.user.driverdetails
    booking_count=DriverBooking.objects.filter(driver=driver).count()
    maintance_count=MaintenanceRequest.objects.filter(driver=driver).count()
    total_count=booking_count+maintance_count
    return render(request,'dropcaro/driver_dashboard.html',{"booking_count":booking_count,"maintance_count":maintance_count,"total_count":total_count})


@login_required
def admin_dashboard_view(request):
    return render(request,'dropcaro/admin_dashboard.html')


def list_my_vehicles(request):
    vehicles = VehicleRegistration.objects.filter(owner__user=request.user)
    return render(request, 'dropcaro/list_my_vehicles.html', {'vehicles': vehicles})


# user_dashboard_view
from django.shortcuts import render


@login_required
def edit_user(request):
    user_details = get_object_or_404(UserDetails, user=request.user)
    if request.method == 'POST':
        form = UserDetailsForm(request.POST, instance=user_details)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')  # Replace 'success_page' with your URL
    else:
        form = UserDetailsForm(instance=user_details)
    return render(request, 'user_dashboard/edit_user.html', {'form': form})


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



# VehicleRegistration view

def vehicle_reg(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        form = VehicleRegistrationForm(request.POST)
        if form.is_valid():
            userds=get_object_or_404(UserDetails,user=request.user)
            vehicle=form.save(commit=False)
            vehicle.owner=userds
            vehicle.save()
            messages.success(request, "Vehicle registered successfully!")
            return redirect('list_my_vehicles')
        else:
            print(form.errors)
            messages.error(request, "Please correct the errors below.")
    else:
        form = VehicleRegistrationForm()

    return render(request, 'dropcaro/vehicle_reg.html', {'form': form})

def driverview(request):
    drivers=DriverDetails.objects.all()
    return render(request, 'user_dashboard/driverview.html',{"drivers":drivers})

def driver_status_update(request):
    driver=request.user.driverdetails
    driver.is_free=not driver.is_free
    driver.save()
    return redirect('driver_dashboard')

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
            Notification.objects.create(
               user=request.user,  # The user who made the booking
               title="Maintance Booking",
               message="Maintance Booking Request Sent",
               customer=request.user
             )
            admin_users = User.objects.filter(is_superuser=True)
            for admin_user in admin_users:
             Notification.objects.create(
                user=admin_user,
                title="New Maintance Booking Request",
             message=f"A booking has been made by {request.user.username}",
                customer=request.user
                )
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
    driver_id = request.GET.get('driver_id')
    status = request.GET.get('status')

    if request.method == "POST":
        driver = get_object_or_404(DriverDetails, id=driver_id)
        user = get_object_or_404(UserDetails, user=request.user)
        form = DriverBookingForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.driver=driver
            obj.user=user
            obj.save()
            Notification.objects.create(
               user=request.user,  # The user who made the booking
               title="Driver Booking",
               message="Driver Booking Request Sent",
               customer=request.user
             )
            Notification.objects.create(user=driver.user,title="Booking request",message="booked",customer=request.user)
            admin_users = User.objects.filter(is_superuser=True)
            for admin_user in admin_users:
             Notification.objects.create(
                user=admin_user,
                title="New Driver Booking Request",
             message=f"A booking has been made by {request.user.username} for driver {driver.user.username}.",
                customer=request.user
                )
            messages.success(request, "Driver booked successfully!")
            return redirect('user_dashboard')  # Redirect to prevent form resubmission
        else:
            print(form.errors)
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = DriverBookingForm()

    drivers=DriverDetails.objects.all()
    return render(request, 'dropcaro/book_driver.html', {'form': form,'drivers':drivers,'driver_id':driver_id,'status':status})


def share_location_view(request,task_id):
    return render(request, 'driver_dashboard/live_location_share.html',{'task_id':task_id})


@csrf_exempt  
def update_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            task_id = data.get('task_id')

            if latitude is None or longitude is None:
                return JsonResponse({"error": "Latitude and longitude are required"}, status=400)

            task = get_object_or_404(DriverBooking, id=task_id)
            location, created = Location.objects.get_or_create(
                task=task
            )

            location.latitude = latitude
            location.longitude = longitude
            location.save()

            response_data = {
                "latitude": latitude,
                "longitude": longitude,
            }

            return JsonResponse(response_data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    return HttpResponse(status=405)

def get_live_location(request, task_id):
    task = get_object_or_404(DriverBooking, id=task_id)
    location = Location.objects.filter(task=task).first()
    if not location:
        return HttpResponse('Location not shared yet', status=404)
    lat=location.latitude
    lon=location.longitude
    print(task,location)
    return render(request,'view_livelocation.html',{"latitude": lat, "longitude": lon,"task_id":task_id})

import random
def view_live_location(request,task_id):
    location = Location.objects.filter(task__id=task_id).first()
    print(task_id)
    location = {"latitude": location.latitude, "longitude": location.longitude}
    return JsonResponse(location)

def driver_booking_history(request): 
    driver_bookings=DriverBooking.objects.filter(user__user=request.user)
    return render(request, 'dropcaro/booking_history.html',{"driver_bookings":driver_bookings})
    
def user_notification(request):
    notifications=Notification.objects.filter(user=request.user)
    return render(request, 'dropcaro/user_notification.html',{"notifications":notifications})

def feedback(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        feedback_type = request.POST['feedback_type']
        message = request.POST['message']

        # Save feedback to the database
        Feedback.objects.create(
            name=name,
            email=email,
            feedback_type=feedback_type,
            message=message
        )
        Notification.objects.create(
               user=request.user,  # The user who made the booking
               title="Feedback sented",
               message="",
               customer=request.user
             )
        # Display success message
        messages.success(request, 'Thank you for your feedback!')
        return redirect('user_dashboard')

    return render(request, 'user_dashboard/feedback.html')


# driver_dashboard
# view task

def view_work(request):
    work=DriverBooking.objects.filter(driver__user=request.user)
    return render(request, 'driver_dashboard/view_work.html',{"work":work})

def view_vehicle(request):
    # Filter by owner if the 'driver' field is not available
    vehicless = VehicleRegistration.objects.filter(owner__user=request.user)
    return render(request, 'driver_dashboard/view_vehicle.html', {"vehicless": vehicless})

def my_maintenance(request):
    bookmaintance=MaintenanceRequest.objects.all()    
    return render(request, 'driver_dashboard/my_maintenance.html',{"bookmaintance":bookmaintance})


@login_required
def edit_driver(request):
    driver_details = get_object_or_404(DriverDetails, user=request.user)
    if request.method == 'POST':
        form = DriverDetailsForm(request.POST, request.FILES, instance=driver_details)
        if form.is_valid():
            form.save()
            return redirect('driver_dashboard')  # Replace 'success_page' with your URL
    else:
        form = DriverDetailsForm(instance=driver_details)
    return render(request, 'driver_dashboard/edit_driver.html', {'form': form})
 

def driver_notification(request):
    notifications=Notification.objects.filter(user=request.user)
    return render(request, 'dropcaro/driver_notification.html',{"notifications":notifications})


def update_status(request):
    Notification.objects.create(
               user=request.user,  # The user who made the booking
               title="yss",
               message="",
               customer=request.user
             )
    return redirect('view_work')

def maintenance_checklist(request):
    return render(request, "driver_dashboard/maintenance_checklist.html")

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

from django.db import transaction

def delete_user(request, user_id):
    with transaction.atomic():  # Use a transaction to ensure the deletion is committed
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, f"User '{user.username}' deleted successfully.")
    return redirect('manage_users')


def delete_driver(request, driver_id):
    driver = get_object_or_404(User, id=driver_id)
    driver.delete()
    messages.success(request, f"User '{driver.username}' deleted successfully.")
    return redirect('manage_driver')


def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    payment.delete()
    messages.success(request, f"Payment with ID '{payment_id}' deleted successfully.")
    return redirect('payment_view')  # Replace 'manage_payments' with your desired redirect URL name


def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(VehicleRegistration, id=vehicle_id)
    vehicle.delete()
    messages.success(request, f"Vehicle '{vehicle.vehicle_number}' deleted successfully.")
    return redirect('vehicle_details')  # Adjust 'manage_vehicles' to match your URL name


def delete_booking(request, booking_id):
    booking = get_object_or_404(DriverBooking, id=booking_id)
    booking.delete()
    messages.success(request, f"Booking with ID '{booking.id}' deleted successfully.")
    return redirect('view_bookdriver')  


def delete_request(request, request_id):
    user_request = get_object_or_404(MaintenanceRequest, id=request_id)
    user_request.delete()
    messages.success(request, f"Request with ID '{user_request.id}' deleted successfully.")
    return redirect('view_bookmaintance') 


def view_bookmaintance(request):
    bookmaintance=MaintenanceRequest.objects.all()
    drivers=DriverDetails.objects.all()
    vehicle_number=request.GET.get('vehicle_number')
    if vehicle_number:
        bookmaintance=bookmaintance.filter(vehicle__vehicle_number__icontains=vehicle_number)
    return render(request, 'admin_dashboard/view_bookmaintance.html',{"bookmaintance":bookmaintance,'drivers':drivers})


def maintainance_history(request,vehicle_id):
    bookmaintance=MaintenanceRequest.objects.filter(vehicle__id=vehicle_id)
    print(bookmaintance,'test')
    return render(request, 'maintainance_history.html',{"bookmaintance":bookmaintance})


def payment_view(request):
    viewpay=Payment.objects.all()
    return render(request, 'admin_dashboard/payment_view.html',{"viewpay":viewpay})


def notification(request):
    notifications=Notification.objects.filter(user=request.user)
    return render(request, 'admin_dashboard/notification.html',{"notifications":notifications})



# payment
from django.shortcuts import get_object_or_404
def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            user=get_object_or_404(UserDetails,user=request.user)
            data=form.save(commit=False)
            data.user=user
            data.save()
            Notification.objects.create(
               user=request.user,  # The user who made the booking
               title="Payment Sucessfully",
               message="",
               customer=request.user
             )
            admin_users = User.objects.filter(is_superuser=True)
            for admin_user in admin_users:
             Notification.objects.create(
                user=admin_user,
                title="Payment Sucessfull",
             message=f"Payed by{request.user.username} amount: {data.amount}",
                customer=request.user
                )            
            return redirect('sucessfull_payment')
    else:
        form = PaymentForm()
    return render(request, 'payment/payment.html',{'form':form})

def sucessfull_payment(request):
    return render(request, 'payment/sucessfull_payment.html')


def admin_assign_maintanance(request,driver_id,booking_id):
    if request.method=='POST':
        driver=get_object_or_404(DriverDetails,id=driver_id)
        booking=get_object_or_404(MaintenanceRequest,id=booking_id)
        booking.driver=driver
        print(driver_id,booking,'kdjsf')
        booking.save()
        Notification.objects.create(
        user=booking.driver.user,
        title="Maintenance Request Update",
        message="A driver has been assigned to your request.",
        customer=booking.vehicle.owner.user
    )
        Notification.objects.create(
         user=driver.user,
         title="maintenance request",
         message="driver assigned",
         customer=booking.vehicle.owner.user if booking.vehicle and booking.vehicle.owner else None
            )

    return redirect('view_bookmaintance')


def add_user(request):
    if request.method == 'POST':
        data = request.POST.copy()
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except Exception as e:
            print(e)
            messages.error(request, 'Error creating user: {}'.format(str(e)))
            return redirect('add_user')
        
        user_form = UserDetailsForm(data)
        if user_form.is_valid():
            user_details = user_form.save(commit=False)
            user_details.user = user
            user_details.save()
            messages.success(request, 'Registration successful!')
            return redirect('manage_users')
        else:
            print(user_form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserDetailsForm()

    return render(request, 'admin_dashboard/add_user.html', {'form': user_form})


def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')  # Fetch all feedbacks and order by latest
    return render(request, 'admin_dashboard/feedback_list.html', {'feedbacks': feedbacks})



