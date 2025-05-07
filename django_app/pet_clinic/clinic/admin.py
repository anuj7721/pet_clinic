from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Clinic, Pet, Appointment, Service, Review

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email')
    search_fields = ('name', 'address', 'phone', 'email')
    filter_horizontal = ('services',)

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'age', 'owner')
    list_filter = ('species',)
    search_fields = ('name', 'breed', 'owner__username')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('pet', 'clinic', 'date', 'time', 'status', 'created_at')
    list_filter = ('status', 'date', 'clinic')
    search_fields = ('pet__name', 'clinic__name', 'reason')
    date_hierarchy = 'date'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'clinic', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'clinic__name', 'comment')
    date_hierarchy = 'created_at'