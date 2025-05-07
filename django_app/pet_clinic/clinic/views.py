from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q, Avg
from .forms import UserRegistrationForm, PetForm, AppointmentForm, ReviewForm, ClinicSearchForm
from .models import Clinic, Appointment, Service, Review

def home(request):
    form = ClinicSearchForm(request.GET)
    clinics = Clinic.objects.all()
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            clinics = clinics.filter(name__icontains=search_query)
    
    return render(request, 'clinic/home.html', {
        'clinics': clinics,
        'search_form': form
    })

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        messages.error(request, "Registration failed. Please check the form.")
    else:
        form = UserRegistrationForm()
    return render(request, 'clinic/signup.html', {'form': form})

@login_required
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            messages.success(request, "Pet added successfully!")
            return redirect('pet_list')
        messages.error(request, "Failed to add pet. Please check the form.")
    else:
        form = PetForm()
    return render(request, 'clinic/pet_form.html', {'form': form})

@login_required
def pet_list(request):
    pets = request.user.pets.all()
    return render(request, 'clinic/pet_list.html', {'pets': pets})

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.user, request.POST)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, "Appointment booked successfully!")
            return redirect('appointment_status', appointment_id=appointment.id)
        messages.error(request, "Failed to book appointment. Please check the form.")
    else:
        form = AppointmentForm(request.user)
    return render(request, 'clinic/appointment_form.html', {'form': form})

@login_required
def appointment_status(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    # Check if the appointment belongs to the user
    if appointment.pet.owner != request.user:
        messages.error(request, "You don't have permission to view this appointment.")
        return redirect('home')
    return render(request, 'clinic/appointment_status.html', {'appointment': appointment})

@login_required
def appointment_list(request):
    # Get all appointments for the user's pets
    appointments = Appointment.objects.filter(pet__owner=request.user)
    return render(request, 'clinic/appointment_list.html', {'appointments': appointments})

# New views for services and reviews
def services_list(request):
    services = Service.objects.all()
    return render(request, 'clinic/services_list.html', {'services': services})

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    clinics = service.clinics.all()
    return render(request, 'clinic/service_detail.html', {
        'service': service,
        'clinics': clinics
    })

def clinic_detail(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    reviews = clinic.reviews.all().order_by('-created_at')
    user_review = None
    
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    
    return render(request, 'clinic/clinic_detail.html', {
        'clinic': clinic,
        'reviews': reviews,
        'user_review': user_review
    })

@login_required
def add_review(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    
    # Check if user already reviewed this clinic
    existing_review = Review.objects.filter(user=request.user, clinic=clinic).first()
    
    if request.method == 'POST':
        if existing_review:
            form = ReviewForm(request.POST, instance=existing_review)
            success_message = "Your review has been updated!"
        else:
            form = ReviewForm(request.POST)
            success_message = "Your review has been added!"
            
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.clinic = clinic
            review.save()
            messages.success(request, success_message)
            return redirect('clinic_detail', clinic_id=clinic.id)
        messages.error(request, "There was an error with your review. Please check the form.")
    else:
        if existing_review:
            form = ReviewForm(instance=existing_review)
        else:
            form = ReviewForm()
    
    return render(request, 'clinic/add_review.html', {
        'form': form,
        'clinic': clinic,
        'is_update': existing_review is not None
    })