from django.contrib import admin
from .models import User, Service, Booking,Payment,Slot

# Register your models here.

admin.site.register(User)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Slot)

