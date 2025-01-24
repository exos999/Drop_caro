from django.urls import path
from. import views


urlpatterns = [
    path('',views.home, name='home'),
    # path('login/',views.login_view, name='login'),
    # path('logout/', views.logout_user, name='logout'),  # Add logout path
    # path('signup/', views.signup_view, name='signup'),
     path('about/', views.about_view, name='about'),
     path('service/', views.service_view, name='service'),
     path('contact/', views.contact_view, name='contact'),
     
     
    # loginview
    
     path('login/', views.login_view, name='login'),
     path('logout/', views.logout_view, name='logout_view'),
     path('accounts/login/', views.login_view, name='login'),
     path('carowner/', views.carowner_registration, name='carowner'),
     path('driver_reg/', views.driver_view, name='driver_reg'),
   
    
    # dashboard
    
     path('user_dashboard/', views.user_dashboard_view, name='user_dashboard'),
     path('driver_dashboard/', views.driver_dashboard_view, name='driver_dashboard'),
     path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
     
     
     
     #  user dash board 
     path('maintenance_reg/', views.maintenance_reg, name='maintenance_reg'),
     path('book_driver/', views.book_driver, name='book_driver'),
     path('vehicle_reg/', views.vehicle_reg, name='vehicle_reg'),
     path('driverview/', views.driverview, name='driverview'),
     path('edit_user/', views.edit_user, name='edit_user'),
     
     path('map/', views.map, name='map'),
     
    # path('', views.home, name='home'),
    # path('track/', views.track_vehicle, name='track'),
    # path('payments/', views.payments, name='payments'),
    path('logout/', views.logout_view, name='logout'),
    
    
    # driverdashboard
    
    path('view_work/', views.view_work, name='view_work'),
    path('view_vehicle/', views.view_vehicle, name='view_vehicle'),
    path('my_maintance/', views.my_maintance, name='my_maintance'),
    path('edit_driver/', views.edit_driver, name='edit_driver'),
    path('driver_notification/', views.driver_notification, name='driver_notification'),

     
  
  
    # admindashboard
    path('manage_users/', views.manage_users, name='manage_users'),
    path('manage_drivers/', views.manage_drivers, name='manage_drivers'),
    path('vehicle_details/', views.vehicle_details, name='vehicle_details'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),  # Change deactivate to delete
    path('delete_driver/<int:driver_id>/', views.delete_driver, name='delete_driver'),  # Change deactivate to delete
    path('delete_vehicle/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('delete-request/<int:request_id>/', views.delete_request, name='delete_request'),

    path('view_bookdriver/', views.view_bookdriver, name='view_bookdriver'),
    path('view_bookmaintance/', views.view_bookmaintance, name='view_bookmaintance'),
    path('admin_assign_maintanance/<int:booking_id>/<int:driver_id>/', views.admin_assign_maintanance, name='admin_assign_maintanance'),

    path('list_vehicles/', views.list_my_vehicles, name='list_vehicles'),
    path('payment_view/', views.payment_view, name='payment_view'),
    
    # payment
    
    path('payment/', views.payment, name='payment'),
    path('sucessfull_payment/', views.sucessfull_payment, name='sucessfull_payment'),
    path('delete_payment/<int:payment_id>/', views.delete_payment, name='delete_payment'),
    path('notification/', views.notification, name='notification'),
    path('share_location_view/<int:task_id>/', views.share_location_view, name='share_location_view'),

    path('update-location', views.update_location, name='update-location'),
    path('driver_booking_history/', views.driver_booking_history, name='driver_booking_history'),
] 