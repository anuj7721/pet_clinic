from flask_restful import Resource, reqparse
from flask import request, jsonify
import json
import os
from datetime import datetime
from .models import AppointmentModel, ServiceModel, ReviewModel

# Data storage file paths
APPOINTMENTS_FILE = 'appointments.json'
SERVICES_FILE = 'services.json'
REVIEWS_FILE = 'reviews.json'

# Helper functions for data persistence
def load_appointments():
    if os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE, 'r') as f:
            return json.load(f)
    return {'appointments': []}

def save_appointments(data):
    with open(APPOINTMENTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_services():
    if os.path.exists(SERVICES_FILE):
        with open(SERVICES_FILE, 'r') as f:
            return json.load(f)
    return {'services': []}

def save_services(data):
    with open(SERVICES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_reviews():
    if os.path.exists(REVIEWS_FILE):
        with open(REVIEWS_FILE, 'r') as f:
            return json.load(f)
    return {'reviews': []}

def save_reviews(data):
    with open(REVIEWS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Request parsers
appointment_parser = reqparse.RequestParser()
appointment_parser.add_argument('pet_id', type=int, required=True, help='Pet ID is required')
appointment_parser.add_argument('clinic_id', type=int, required=True, help='Clinic ID is required')
appointment_parser.add_argument('date', type=str, required=True, help='Date is required (YYYY-MM-DD)')
appointment_parser.add_argument('time', type=str, required=True, help='Time is required (HH:MM:SS)')
appointment_parser.add_argument('reason', type=str, required=True, help='Reason for visit is required')
appointment_parser.add_argument('status', type=str)

service_parser = reqparse.RequestParser()
service_parser.add_argument('name', type=str, required=True, help='Service name is required')
service_parser.add_argument('description', type=str, required=True, help='Service description is required')
service_parser.add_argument('icon', type=str)

review_parser = reqparse.RequestParser()
review_parser.add_argument('user_id', type=int, required=True, help='User ID is required')
review_parser.add_argument('clinic_id', type=int, required=True, help='Clinic ID is required')
review_parser.add_argument('rating', type=int, required=True, help='Rating is required (1-5)')
review_parser.add_argument('comment', type=str, required=True, help='Comment is required')

# API Resources
class AppointmentListResource(Resource):
    def get(self):
        """Get all appointments"""
        data = load_appointments()
        return jsonify(data['appointments'])
    
    def post(self):
        """Create a new appointment"""
        args = appointment_parser.parse_args()
        data = load_appointments()
        
        # Create a new appointment
        new_appointment = {
            'id': len(data['appointments']) + 1,
            'pet_id': args['pet_id'],
            'clinic_id': args['clinic_id'],
            'date': args['date'],
            'time': args['time'],
            'reason': args['reason'],
            'status': args.get('status', 'PENDING'),
            'created_at': datetime.now().isoformat()
        }
        
        # Add the appointment to the data store
        data['appointments'].append(new_appointment)
        save_appointments(data)
        
        return new_appointment, 201


class AppointmentResource(Resource):
    def get(self, appointment_id):
        """Get a specific appointment by ID"""
        data = load_appointments()
        for appointment in data['appointments']:
            if appointment['id'] == appointment_id:
                return appointment
        return {'error': 'Appointment not found'}, 404
    
    def put(self, appointment_id):
        """Update a specific appointment by ID"""
        args = appointment_parser.parse_args(strict=False)  # Allow partial updates
        data = load_appointments()
        
        for i, appointment in enumerate(data['appointments']):
            if appointment['id'] == appointment_id:
                # Update only the fields that were provided
                for key, value in args.items():
                    if value is not None:
                        data['appointments'][i][key] = value
                
                save_appointments(data)
                return data['appointments'][i]
        
        return {'error': 'Appointment not found'}, 404
    
    def delete(self, appointment_id):
        """Delete a specific appointment by ID"""
        data = load_appointments()
        
        for i, appointment in enumerate(data['appointments']):
            if appointment['id'] == appointment_id:
                deleted = data['appointments'].pop(i)
                save_appointments(data)
                return {'message': f'Appointment {appointment_id} deleted successfully'}
        
        return {'error': 'Appointment not found'}, 404


class ServiceListResource(Resource):
    def get(self):
        """Get all services"""
        data = load_services()
        return jsonify(data['services'])
    
    def post(self):
        """Create a new service"""
        args = service_parser.parse_args()
        data = load_services()
        
        # Create a new service
        new_service = {
            'id': len(data['services']) + 1,
            'name': args['name'],
            'description': args['description'],
            'icon': args.get('icon')
        }
        
        # Add the service to the data store
        data['services'].append(new_service)
        save_services(data)
        
        return new_service, 201


class ServiceResource(Resource):
    def get(self, service_id):
        """Get a specific service by ID"""
        data = load_services()
        for service in data['services']:
            if service['id'] == service_id:
                return service
        return {'error': 'Service not found'}, 404
    
    def put(self, service_id):
        """Update a specific service by ID"""
        args = service_parser.parse_args(strict=False)  # Allow partial updates
        data = load_services()
        
        for i, service in enumerate(data['services']):
            if service['id'] == service_id:
                # Update only the fields that were provided
                for key, value in args.items():
                    if value is not None:
                        data['services'][i][key] = value
                
                save_services(data)
                return data['services'][i]
        
        return {'error': 'Service not found'}, 404
    
    def delete(self, service_id):
        """Delete a specific service by ID"""
        data = load_services()
        
        for i, service in enumerate(data['services']):
            if service['id'] == service_id:
                deleted = data['services'].pop(i)
                save_services(data)
                return {'message': f'Service {service_id} deleted successfully'}
        
        return {'error': 'Service not found'}, 404


class ReviewListResource(Resource):
    def get(self):
        """Get all reviews"""
        data = load_reviews()
        return jsonify(data['reviews'])
    
    def post(self):
        """Create a new review"""
        args = review_parser.parse_args()
        data = load_reviews()
        
        # Validate rating range
        if args['rating'] < 1 or args['rating'] > 5:
            return {'error': 'Rating must be between 1 and 5'}, 400
        
        # Check if user already reviewed this clinic
        for review in data['reviews']:
            if review['user_id'] == args['user_id'] and review['clinic_id'] == args['clinic_id']:
                return {'error': 'User has already reviewed this clinic'}, 400
        
        # Create a new review
        new_review = {
            'id': len(data['reviews']) + 1,
            'user_id': args['user_id'],
            'clinic_id': args['clinic_id'],
            'rating': args['rating'],
            'comment': args['comment'],
            'created_at': datetime.now().isoformat()
        }
        
        # Add the review to the data store
        data['reviews'].append(new_review)
        save_reviews(data)
        
        return new_review, 201


class ReviewResource(Resource):
    def get(self, review_id):
        """Get a specific review by ID"""
        data = load_reviews()
        for review in data['reviews']:
            if review['id'] == review_id:
                return review
        return {'error': 'Review not found'}, 404
    
    def put(self, review_id):
        """Update a specific review by ID"""
        args = review_parser.parse_args(strict=False)  # Allow partial updates
        data = load_reviews()
        
        # Validate rating range if provided
        if args.get('rating') is not None and (args['rating'] < 1 or args['rating'] > 5):
            return {'error': 'Rating must be between 1 and 5'}, 400
        
        for i, review in enumerate(data['reviews']):
            if review['id'] == review_id:
                # Update only the fields that were provided
                for key, value in args.items():
                    if value is not None:
                        data['reviews'][i][key] = value
                
                save_reviews(data)
                return data['reviews'][i]
        
        return {'error': 'Review not found'}, 404
    
    def delete(self, review_id):
        """Delete a specific review by ID"""
        data = load_reviews()
        
        for i, review in enumerate(data['reviews']):
            if review['id'] == review_id:
                deleted = data['reviews'].pop(i)
                save_reviews(data)
                return {'message': f'Review {review_id} deleted successfully'}
        
        return {'error': 'Review not found'}, 404


class ClinicReviewsResource(Resource):
    def get(self, clinic_id):
        """Get all reviews for a specific clinic"""
        data = load_reviews()
        clinic_reviews = [
            review for review in data['reviews']
            if review['clinic_id'] == clinic_id
        ]
        return jsonify(clinic_reviews)


class UserReviewsResource(Resource):
    def get(self, user_id):
        """Get all reviews by a specific user"""
        data = load_reviews()
        user_reviews = [
            review for review in data['reviews']
            if review['user_id'] == user_id
        ]
        return jsonify(user_reviews)


class ClinicServicesResource(Resource):
    def get(self, clinic_id):
        """Get all services offered by a specific clinic"""
        # In a real app, this would query a clinic-service relationship table
        # For simplicity, we'll return all services
        data = load_services()
        return jsonify(data['services'])


class HealthCheckResource(Resource):
    def get(self):
        """Simple health check endpoint"""
        return {
            'status': 'ok',
            'message': 'Flask API is running',
            'timestamp': datetime.now().isoformat()
        }