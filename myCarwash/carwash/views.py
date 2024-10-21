from django.shortcuts import render, redirect, get_object_or_404
from .models import User,Service,Booking,Payment,Slot
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q


# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(user_name=username)  # Adjust this based on your User model field
            # Check if the password is correct
            if user.user_pass == password:  # It's better to use Django's built-in password checking
                  # Log the user in
                if user.role == 'Customer':
                     return redirect('customerMain', user_id=user.user_id)
                elif user.role == 'Staff':
                    return redirect('staffMain', user_id=user.user_id)  # Redirect staff to their main page
                elif user.role == 'Admin':
                    return redirect('adminMain', user_id=user.user_id)  # Redirect admin to their main page
            else:
                messages.error(request, 'Invalid username or password.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'carwash/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST['phone']

        # Check if the username already exists
        if User.objects.filter(user_name=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        # Create a new user
        user = User.objects.create(user_name=username, user_pass=password)
        # Optionally, save the phone number to the user profile if you have a profile model
        # user.profile.phone = phone
        # user.profile.save()
        
        messages.success(request, "You have successfully signed up. Please log in.")
        return redirect('login')  # Redirect to the login page after signup
    
    return render(request, 'carwash/signup.html')

def logout(request):
    return redirect('login')

def user_view_booking(request,user_id):
    try:
        user = User.objects.filter(user_id=user_id).values()
        selectedUser = User.objects.get(user_id = user_id)
        app = Booking.objects.filter(booking_id=selectedUser.user_id).values
        service = Service.objects.all().values()
        slots = Slot.objects.all().values()
        user_details = {
            'userDetails': user,
            # 'details': details,
            'user_id':user_id,
            'selectedUser':selectedUser,
            'Allbooking':app,
            'AllServices':service,
            'slots':slots
            
        }

        return render(request, 'carwash/customerBooking.html', user_details)
    except User.DoesNotExist:
        return HttpResponse("User Not Found")


def user_post_booking(request,user_id):

    user = User.objects.get(user_id=user_id)
    context = {
        'selectedUser':user
    }
    return render(request, 'carwash/customerBooking.html',context )

def submitBooking(request, user_id):
    if request.method == 'POST':
        # Retrieve form data
        vehicle_type = request.POST['vehicle_type']
        car_plate = request.POST['car_plate']
        phone_number = request.POST['phone_number']
        slot = request.POST['slot']
        service_id = request.POST['service_package']
        
        # Fetch the selected service object
        service = get_object_or_404(Service, service_id=service_id)
        
        # Fetch the customer (Assuming the customer exists in the database based on user_id)
        customer = get_object_or_404(User, user_id=user_id)

        # Create and save the booking object
        booking = Booking(
            customer=customer,
            vehicle_type=vehicle_type,
            no_plate = car_plate,
            no_phone = phone_number,
            slot=slot,
            service=service
        )
        booking.save()

        # Success message
        messages.success(request, 'Your booking has been successfully submitted!')

        # Redirect to the customer main page or a success page
        return redirect('customerMain', user_id=user_id)
    
    # If GET request, render the booking form again (this is optional)
    return render(request, 'customer_page.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from django.contrib import messages

# Edit Booking View (No form used)
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    services = Service.objects.all().values()  
    if request.method == 'POST':
        service = request.POST.get('service_package')
        slot = request.POST.get('slot')
        vehicle_type = request.POST.get('vehicle_type')
        no_plate = request.POST.get('car_plate')

        # Update the booking details with the new data from the POST request
        booking.service_id = service
        booking.slot = slot
        booking.vehicle_type = vehicle_type
        booking.no_plate = no_plate
        booking.save()

        messages.success(request, 'Booking updated successfully!')
        return redirect('customerMain', user_id=request.user.id)

    context = {
        'booking': booking,
        'AllServices':services,
        'user_id':request.user.id
               }
    return render(request, 'carwash/customerEdit.html',context)

# Cancel Booking View (remains unchanged)
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)

    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking cancelled successfully!')
        return redirect('customerMain', user_id=request.user.id)

    return render(request, 'cancel_booking_confirm.html', {'booking': booking})
   

def booking_success(request):
    return render(request, 'carwash/bookingSuccess.html')

    
# in this homepage of customer there is User name and also there is a view booking reservation that has been made by the customer    
def showCustomerMain(request, user_id):
        booking = Booking.objects.filter(customer_id=user_id).values()
        services = Service.objects.all().values()
        #depan database belakang nak bawak apa
        context = {
            "user_id" : user_id,
            "bookingDetails":booking,
            "serviceDetails":services,
        }
        
        return render(request, 'carwash/customerMain.html', context)




def showStaffMain(request, user_id):
    services = Service.objects.all().values()
    user = User.objects.get(user_id=user_id)
    booking = Booking.objects.filter(status='Not yet').values()
    context = {
        "Allservices":services,
        'userDetails':user,
        'allBooking':booking,
        'user_id':user_id,
    }
    return render(request,"carwash/staffMain.html",context)

def staff_view(request, user_id):
    userDetails = User.objects.get(user_id=user_id) 
    bookingDetails = Booking.objects.all().values()
    
    obj ={
        "mode":"customer",
        "userDetails": userDetails,
        "bookingDetails": bookingDetails,
        
    }

    return render(request, 'carwash/staffMain.html', obj)

def approve_booking(request,user_id,booking_id):

    booking = Booking.objects.get(booking_id=booking_id)
    booking.status="Done"
    booking.save()
    return redirect ('staffMain',user_id)

def showAdminMain(request, user_id):
    services = Service.objects.all().values()
    user = User.objects.get(user_id=user_id)
    booking = Booking.objects.filter(status='Not yet').values()
    
    # Fetch all staff members
    staff_members = User.objects.filter(role='Staff').values()

    context = {
        "Allservices": services,
        'userDetails': user,
        'allBooking': booking,
        'user_id': user_id,
        'staff_members': staff_members,  # Pass staff members to the context
    }
    return render(request, "carwash/AdminMain.html", context)



import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import User, Service

@csrf_exempt  # Use with caution; remove in production and handle CSRF properly
def  update_service(request, user_id):
    if request.method == "POST":
        data = json.loads(request.body)
        service_id = data.get('service_id')
        service_name = data.get('service_name')
        price = data.get('price')

        try:
            service = Service.objects.get(service_id=service_id)
            service.service_name = service_name
            service.price = price
            service.save()

            return JsonResponse({'success': True})
        except Service.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found'})

    # Handle GET request or render the page
    userDetails = User.objects.get(user_id=user_id)
    services = Service.objects.all().values()
    context = {
        "userDetails": userDetails,
        "Allservices": services,
    }
    return render(request, 'carwash/update_service.html', context)


from django.http import JsonResponse

# Existing imports...

@csrf_exempt  # Use with caution; remove in production and handle CSRF properly
def delete_service(request, service_id):
    try:
        service = Service.objects.get(service_id=service_id)
        service.delete()
        return JsonResponse({'success': True})
    except Service.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Service not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Service
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Use with caution; remove in production and handle CSRF properly
def add_service(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)

            service_name = body_data.get('service_name')
            price = body_data.get('price')

            if not service_name or price is None:
                return JsonResponse({'success': False, 'error': 'Service name and price are required'})

            new_service = Service.objects.create(service_name=service_name, price=price)

            return JsonResponse({'success': True, 'service': {
                'service_id': new_service.service_id,
                'service_name': new_service.service_name,
                'price': str(new_service.price),
            }})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Service

def edit_service(request, service_id):
    # Get the service by ID
    service = get_object_or_404(Service, service_id=service_id)

    if request.method == 'POST':
        # Retrieve form data
        service_name = request.POST.get('name')  # Changed from service_name to name
        price = request.POST.get('price')

        # Validate that service_name is not None or empty
        if not service_name:
            messages.error(request, 'Service name cannot be empty.')
            return render(request, 'carwash/edit_service.html', {'service': service})

        # Update the service details
        service.service_name = service_name
        service.price = price
       
        # Save the updated service
        service.save()

        # Success message
        messages.success(request, 'Service updated successfully!')
        return redirect('edit_service', service_id=service_id)

    # If GET request, render the form with the current service details
    context = {
        'service': service,
        'user_id': request.user.id,
        
        
    }
    return render(request, 'carwash/edit_service.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def addStaff(request, user_id):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        phone = request.POST['phone']
        
        # Check if the staff member already exists
        if User.objects.filter(user_name=name).exists():
            messages.error(request, 'Staff member with this name already exists.')
            return redirect('staffPage', user_id=user_id)  # Redirect back to staff page if error
        
        # Create a new staff member with role 'Staff'
        new_staff = User(user_name=name, user_pass=password, no_phone=phone, role='Staff')
        new_staff.save()

        messages.success(request, 'New staff member added successfully!')
        return redirect('adminMain', user_id=user_id)  # Redirect to admin main page after adding staff

    return render(request, 'carwash/staffPage.html', {'user_id': user_id})




def staffPage(request, user_id):
    # Render the staffPage for adding a new staff
    user = User.objects.get(user_id=user_id)  # Fetch the admin user by their user_id
    context = {
        'user_id': user.user_id,  # Pass the user ID for the admin
    }
    return render(request, 'carwash/staffPage.html', context)

from django.db.models import Sum
from .models import Booking, Service

def reportBooking(request):
    bookings = Booking.objects.all()  # Assuming you have a Booking model
    total_price = sum([booking.service.price for booking in bookings])  # Calculate total price
    total_booking = bookings.count()  # Count the total number of bookings
    
    context = {
        'bookings': bookings,
        'Allservices': Service.objects.all(),  # Assuming you have a Service model
        'total_price': total_price,
        'total_booking': total_booking,  # Pass the total number of bookings to the template
    }
    return render(request, 'carwash/reportBooking.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import User  # Assuming the model is User for staff members

def edit_staff(request, user_id):
    # Get the staff member by user_id
    staff_member = get_object_or_404(User, user_id=user_id)

    if request.method == 'POST':
        # Retrieve form data from the POST request
        staff_name = request.POST.get('name')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone')

        # Validate that none of the fields are empty
        if not staff_name:
            messages.error(request, 'Staff name cannot be empty.')
            return render(request, 'carwash/edit_staff.html', {'staff_member': staff_member})

        if not password:
            messages.error(request, 'Password cannot be empty.')
            return render(request, 'carwash/edit_staff.html', {'staff_member': staff_member})

        if not phone_number:
            messages.error(request, 'Phone number cannot be empty.')
            return render(request, 'carwash/edit_staff.html', {'staff_member': staff_member})

        # Update the staff member's details
        staff_member.user_name = staff_name
        staff_member.user_pass = password  # Ensure you're hashing passwords if necessary
        staff_member.no_phone = phone_number

        # Save the updated staff member details
        staff_member.save()

        # Success message
        messages.success(request, 'Staff details updated successfully!')
        return redirect('adminMain', user_id=request.user.id)  # Redirect back to the admin page

    # If GET request, render the form with the current staff details
    context = {
        'staff_member': staff_member,
    }
    return render(request, 'carwash/edit_staff.html', context)

from django.http import JsonResponse
from django.views.decorators.http import require_POST

@require_POST
def cancel_staff(request, user_id):
    try:
        staff = get_object_or_404(User, user_id=user_id)  # Ensure to import your Staff model
        staff.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

def payment_customer(request, user_id):
    bookings = Booking.objects.all()
    context = {
        'bookings': bookings,
        'Allservices': Service.objects.all(),
    }
    return render(request, 'carwash/paymentCustomer.html', context)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Booking

def process_payment(request, user_id):
    if request.method == 'POST':
        payment_proof = request.FILES.get('payment_proof')  # Get uploaded file
        booking_id = request.POST.get('booking_id')  # Get booking ID from form
        payment_method = request.POST.get('payment_method')  # Get payment method

        # Retrieve the booking and update payment status
        booking = get_object_or_404(Booking, booking_id=booking_id)

        # Save payment details
        booking.payment_status = True
        booking.payment_proof = payment_proof
        booking.payment_method = payment_method
        booking.save()

        # Return JSON response for success
        return JsonResponse({"status": "success", "message": "Payment completed"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
    
from django.shortcuts import render

def update_slot(request,user_id):
    # Add logic here to handle updating the slots if needed
    allSlots = Slot.objects.all().values()

    context = {
        "slots":allSlots,
        "selected_user":user_id
    }

    return render(request, 'carwash/updateSlot.html',context)

def updating_slot(request, user_id):
    if request.method == "POST":
        slotId = request.POST['slot']
        availability = int(request.POST['slot_status'])  # Convert to integer

        slot = Slot.objects.get(id=slotId)
        if availability == 1:
            slot.slot_status = 1
        else:
            slot.slot_status = 0

        slot.save()

    return redirect('update_slot', user_id=user_id)



















