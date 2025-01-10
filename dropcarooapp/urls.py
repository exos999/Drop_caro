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
     
     path('map/', views.map, name='map'),
     
    # path('', views.home, name='home'),
    # path('track/', views.track_vehicle, name='track'),
    # path('payments/', views.payments, name='payments'),
    # path('logout/', views.logout_view, name='logout'),
    
    
    # driverdashboard
    
    path('view_task/', views.view_task, name='view_task'),
     
  
  
    # admindashboard
    path('manage_users/', views.manage_users, name='manage_users'),
    path('manage_drivers/', views.manage_drivers, name='manage_drivers'),
    path('vehicle_details/', views.vehicle_details, name='vehicle_details'),

   


    path('view_bookdriver/', views.view_bookdriver, name='view_bookdriver'),
    path('view_bookmaintance/', views.view_bookmaintance, name='view_bookmaintance'),
    
    
    # payment
    
    path('payment/', views.payment, name='payment'),
    path('sucessfull_payment/', views.sucessfull_payment, name='sucessfull_payment'),
      
      
]