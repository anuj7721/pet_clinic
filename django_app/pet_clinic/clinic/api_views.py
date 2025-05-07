from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pet, Clinic, Service
from .forms import AppointmentForm, ReviewForm
from .services import (
    # Appointment services
    get_appointments_from_api,
    get_appointment_from_api,
    create_appointment_via_api,
    update_appointment_via_api,
    delete_appointment_via_api,
    
    # Service services
    get_services_from_api,
    get_service_from_api,
    get_clinic_services_from_api,
    
    # Review services
    get_reviews_from_api,
    get_clinic_reviews_from_api,
    create_review_via_api,
    update_review_via_api
)

# Appointment API views
@login_required
def api_appointment_list(request):
    # Get all appointments from the API
    api_appointments = get_appointments_from_api()
    
    # Filter appointments for the current user's pets
    user_pet_ids = Pet.objects.filter(owner=request.user).values_list('id', flat=True)
    user_appointments = [
        appointment for appointment in api_appointments
        if int(appointment.get('pet_id')) in user_pet_ids
    ]
    
    return render(request, 'clinic/api_appointment_list.html', {
        'appointments': user_appointments
    })

@login_required
def api_appointment_detail(request, appointment_id):
    # Get the appointment from the API
    appointment = get_appointment_from_api(appointment_id)
    
    if not appointment:
        messages.error(request, "Appointment not found.")
        return redirect('api_appointment_list')
    
    # Check if the appointment belongs to one of the user's pets
    try:
        pet = Pet.objects.get(id=appointment.get('pet_id'))
        if pet.owner != request.user:
            messages.error(request, "You don't have permission to view this appointment.")
            return redirect('api_appointment_list')
    except Pet.DoesNotExist:
        messages.error(request, "Pet not found.")
        return redirect('api_appointment_list')
    
    # Get the clinic details
    try:
        clinic = Clinic.objects.get(id=appointment.get('clinic_id'))
    except Clinic.DoesNotExist:
        clinic = None
    
    return render(request, 'clinic/api_appointment_detail.html', {
        'appointment': appointment,
        'pet': pet,
        'clinic': clinic
    })

@login_required
def api_book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.user, request.POST)
        if form.is_valid():
            # Prepare data for the API
            appointment_data = {
                'pet_id': form.cleaned_data['pet'].id,
                'clinic_id': form.cleaned_data['clinic'].id,
                'date': form.cleaned_data['date'].strftime('%Y-%m-%d'),
                'time': form.cleaned_data['time'].strftime('%H:%M:%S'),
                'reason': form.cleaned_data['reason']
            }
            
            # Create appointment via API
            new_appointment = create_appointment_via_api(appointment_data)
            
            if new_appointment:
                messages.success(request, "Appointment booked successfully!")
                return redirect('api_appointment_detail', appointment_id=new_appointment['id'])
            else:
                messages.error(request, "Failed to book appointment. Please try again.")
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = AppointmentForm(request.user)
    
    return render(request, 'clinic/api_appointment_form.html', {'form': form})

@login_required
def api_update_appointment(request, appointment_id):
    # Get the appointment from the API
    appointment = get_appointment_from_api(appointment_id)
    
    if not appointment:
        messages.error(request, "Appointment not found.")
        return redirect('api_appointment_list')
    
    # Check if the appointment belongs to one of the user's pets
    try:
        pet = Pet.objects.get(id=appointment.get('pet_id'))
        if pet.owner != request.user:
            messages.error(request, "You don't have permission to update this appointment.")
            return redirect('api_appointment_list')
    except Pet.DoesNotExist:
        messages.error(request, "Pet not found.")
        return redirect('api_appointment_list')
    
    if request.method == 'POST':
        # Only allow updating the status (e.g., cancelling)
        status = request.POST.get('status')
        if status:
            result = update_appointment_via_api(appointment_id, {'status': status})
            if result:
                messages.success(request, "Appointment updated successfully!")
                return redirect('api_appointment_detail', appointment_id=appointment_id)
            else:
                messages.error(request, "Failed to update appointment. Please try again.")
    
    return render(request, 'clinic/api_appointment_update.html', {
        'appointment': appointment,
        'pet': pet
    })

@login_required
def api_cancel_appointment(request, appointment_id):
    # Get the appointment from the API
    appointment = get_appointment_from_api(appointment_id)
    
    if not appointment:
        messages.error(request, "Appointment not found.")
        return redirect('api_appointment_list')
    
    # Check if the appointment belongs to one of the user's pets
    try:
        pet = Pet.objects.get(id=appointment.get('pet_id'))
        if pet.owner != request.user:
            messages.error(request, "You don't have permission to cancel this appointment.")
            return redirect('api_appointment_list')
    except Pet.DoesNotExist:
        messages.error(request, "Pet not found.")
        return redirect('api_appointment_list')
    
    if request.method == 'POST':
        result = update_appointment_via_api(appointment_id, {'status': 'CANCELLED'})
        if result:
            messages.success(request, "Appointment cancelled successfully!")
            return redirect('api_appointment_list')
        else:
            messages.error(request, "Failed to cancel appointment. Please try again.")
    
    return render(request, 'clinic/api_appointment_cancel.html', {
        'appointment': appointment,
        'pet': pet
    })

# Service API views
def api_services_list(request):
    # Get all services from the API
    services = get_services_from_api()
    return render(request, 'clinic/api_services_list.html', {'services': services})

def api_service_detail(request, service_id):
    # Get the service from the API
    service = get_service_from_api(service_id)
    
    if not service:
        messages.error(request, "Service not found.")
        return redirect('api_services_list')
    
    # Get clinics that offer this service
    # In a real app, this would query a clinic-service relationship
    # For simplicity, we'll show all clinics
    clinics = Clinic.objects.all()
    
    return render(request, 'clinic/api_service_detail.html', {
        'service': service,
        'clinics': clinics
    })

# Review API views
@login_required
def api_add_review(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    
    # Get existing reviews for this clinic
    clinic_reviews = get_clinic_reviews_from_api(clinic_id)
    
    # Check if user already reviewed this clinic
    user_review = next((review for review in clinic_reviews if review.get('user_id') == request.user.id), None)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_data = {
                'user_id': request.user.id,
                'clinic_id': clinic_id,
                'rating': form.cleaned_data['rating'],
                'comment': form.cleaned_data['comment']
            }
            
            if user_review:
                # Update existing review
                result = update_review_via_api(user_review['id'], review_data)
                success_message = "Your review has been updated!"
            else:
                # Create new review
                result = create_review_via_api(review_data)
                success_message = "Your review has been added!"
            
            if result:
                messages.success(request, success_message)
                return redirect('clinic_detail', clinic_id=clinic.id)
            else:
                messages.error(request, "There was an error with your review. Please try again.")
        else:
            messages.error(request, "There was an error with your review. Please check the form.")
    else:
        if user_review:
            # Pre-fill form with existing review data
            form = ReviewForm(initial={
                'rating': user_review['rating'],
                'comment': user_review['comment']
            })
        else:
            form = ReviewForm()
    
    return render(request, 'clinic/api_add_review.html', {
        'form': form,
        'clinic': clinic,
        'is_update': user_review is not None
    })