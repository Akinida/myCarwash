from . import views
from django.urls import path

urlpatterns = [
    #Customer
    path("", views.login, name='login'),
    path("signup", views.signup, name='signup'),
    path("logout", views.logout, name='logout'),
    path("customer/<str:user_id>", views.showCustomerMain, name='customerMain'),
    path('customer/<str:user_id>/booking/', views.user_view_booking, name='booking'),
    path('customer/booking/submit/<str:user_id>', views.submitBooking, name='submitBooking'),
    # path('customer/booking/post/<str:user_id>', views.user_post_booking, name='userBooking'),

    path('booking/edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('booking/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    path('payment/<int:user_id>/', views.payment_customer, name='payment_customer'),
    # Add this to handle POST requests from the payment form
    path('payment/<int:user_id>/', views.payment_customer, name='process_payment'),

    # path('confirm_payment/<int:booking_id>/', views.confirm_payment, name='confirm_payment'),  # For payment confirmation



    #Staff

    path('Staff/<str:user_id>', views.showStaffMain, name='staffMain'),
    path('Staff/<str:user_id>/approve/<str:booking_id>', views.approve_booking, name='approve_booking'),
    path('Staff/myCustomer/<str:user_id>', views.staff_view, name='staff'),
    path('Staff/<int:user_id>/updateSlot/', views.update_slot, name='update_slot'),
    path('Staff/<int:user_id>/updateSlot/update', views.updating_slot, name='updating_slot'),


    path('Staff/<str:user_id>/updateService', views.update_service, name='update_service'),
    path('service/edit/<int:service_id>/', views.edit_service, name='edit_service'),

    path('Staff/deleteService/<int:service_id>/', views.delete_service, name='delete_service'), 
    path('Staff/addService/', views.add_service, name='add_service'), 

    #Admin

    path('Admin/<str:user_id>', views.showAdminMain, name="adminMain"),
    path('Admin/staff/add/<str:user_id>', views.addStaff, name="add_staff"),  # Add new staff
    path('Admin/<str:user_id>', views.staffPage, name="staffPage"),  # Staff creation page
    path('report/', views.reportBooking, name='reportBooking'),
    path('Admin/edit/<str:user_id>/', views.edit_staff, name='edit_staff'),
    path('cancel_staff/<int:user_id>/', views.cancel_staff, name='cancel_staff'),

]