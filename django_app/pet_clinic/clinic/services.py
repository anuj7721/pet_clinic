import requests
import json
from django.conf import settings

# Flask API URL (in production, this would be an environment variable)
API_BASE_URL = 'http://localhost:5000/api'

# Appointment services
def get_appointments_from_api():
    """Fetch all appointments from the Flask API"""
    try:
        response = requests.get(f'{API_BASE_URL}/appointments')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching appointments: {e}")
        return []

def get_appointment_from_api(appointment_id):
    """Fetch a specific appointment from the Flask API"""
    try:
        response = requests.get(f'{API_BASE_URL}/appointments/{appointment_id}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching appointment {appointment_id}: {e}")
        return None

def create_appointment_via_api(appointment_data):
    """Create a new appointment via the Flask API"""
    try:
        response = requests.post(
            f'{API_BASE_URL}/appointments',
            json=appointment_data,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating appointment: {e}")
        return None

def update_appointment_via_api(appointment_id, update_data):
    """Update an appointment via the Flask API"""
    try:
        response = requests.put(
            f'{API_BASE_URL}/appointments/{appointment_id}',
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error updating appointment {appointment_id}: {e}")
        return None

def delete_appointment_via_api(appointment_id):
    """Delete an appointment via the Flask API"""
    try:
        response = requests.delete(f'{API_BASE_URL}/appointments/{appointment_id}')
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error deleting appointment {appointment_id}: {e}")
        return False

# Service services
def get_services_from_api():
    """Fetch all services from the Flask API"""
    try:
        response = requests.get(f'{API_BASE_URL}/services')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching services: {e}")
        return []

def get_service_from_api(service_id):
    """Fetch a specific service from the Flask API"""
    try:
        response = requests.get(f'{API_BASE_URL}/services/{service_id}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching service {service_id}: {e}")
        return None

def get_clinic_services_from_api(clinic_id):
    """Fetch all services for a specific clinic from the Flask API"""
    try:
        response = requests.get(f'{API_BASE_URL}/clinics/{clinic_id}/services')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching services for clinic {clinic_id}: {e}")
        return []

# Review services
def get_reviews_from_api():
    """Fetch all reviews from the Flask API"""
    try:
        response = requests.get(f'{API_BASE_URL}/reviews')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching reviews: {e}")
        return []

def get_clinic_reviews_from_api(clinic_id):
    """Fetch all reviews for a specific clinic from the Flask API"""
    try:
        response = requests.get(f'{API_BASE_URL}/clinics/{clinic_id}/reviews')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching reviews for clinic {clinic_id}: {e}")
        return []

def create_review_via_api(review_data):
    """Create a new review via the Flask API"""
    try:
        response = requests.post(
            f'{API_BASE_URL}/reviews',
            json=review_data,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating review: {e}")
        return None

def update_review_via_api(review_id, update_data):
    """Update a review via the Flask API"""
    try:
        response = requests.put(
            f'{API_BASE_URL}/reviews/{review_id}',
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error updating review {review_id}: {e}")
        return None