from django.contrib import admin
from.models import*
from.models import DriverDetails,UserDetails,VehicleRegistration,MaintenanceRequest,DriverBooking

# admin.site.register(Car_owner)
# admin.site.register(UserProfile)
admin.site.register(DriverDetails)
admin.site.register(UserDetails)
admin.site.register(VehicleRegistration)
admin.site.register(MaintenanceRequest)
admin.site.register(DriverBooking)

