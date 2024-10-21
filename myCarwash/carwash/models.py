from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    user_pass = models.CharField(max_length=100)
    no_phone = models.CharField(max_length=100,null=True,blank=True)
    no_plate = models.CharField(max_length=15,null=True)
    role = models.CharField(max_length=20, default='Customer')

class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    vehicle_type = models.CharField(null=True,max_length=20)
    no_plate = models.CharField(max_length=15,null=True,blank=True)
    no_phone = models.CharField(max_length=100,null=True,blank=True)
    slot = models.CharField(null=True, max_length=50)
    status = models.CharField(max_length=100,default="Not yet")
    payment_status = models.BooleanField(default=False) 
    payment_proof = models.FileField(upload_to='payment_receipts/', null=True, blank=True)


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)   

class Slot(models.Model):
    slot_status = models.BooleanField(default=False)
    slot_time = models.TimeField()  