from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, api_views

urlpatterns = [
    # Regular Django views
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='clinic/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/add/', views.add_pet, name='add_pet'),
    
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/<int:appointment_id>/', views.appointment_status, name='appointment_status'),
    
    # New URLs for services and reviews
    path('services/', views.services_list, name='services_list'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('clinics/<int:clinic_id>/', views.clinic_detail, name='clinic_detail'),
    path('clinics/<int:clinic_id>/review/', views.add_review, name='add_review'),
    
    # Flask API integration views
    path('api/appointments/', api_views.api_appointment_list, name='api_appointment_list'),
    path('api/appointments/book/', api_views.api_book_appointment, name='api_book_appointment'),
    path('api/appointments/<int:appointment_id>/', api_views.api_appointment_detail, name='api_appointment_detail'),
    path('api/appointments/<int:appointment_id>/update/', api_views.api_update_appointment, name='api_update_appointment'),
    path('api/appointments/<int:appointment_id>/cancel/', api_views.api_cancel_appointment, name='api_cancel_appointment'),
]