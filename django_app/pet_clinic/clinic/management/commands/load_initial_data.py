from django.core.management.base import BaseCommand
from clinic.models import Service, Clinic
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    help = 'Loads initial data for the Pet Clinic Finder app'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Loading initial data...')
        
        # Create services
        services_data = [
            {
                'name': 'Wellness Exams',
                'description': 'Regular check-ups to ensure your pet is healthy and to catch any potential issues early.',
                'icon': 'stethoscope'
            },
            {
                'name': 'Vaccinations',
                'description': 'Protection against common and serious diseases that can affect your pet.',
                'icon': 'syringe'
            },
            {
                'name': 'Dental Care',
                'description': 'Dental cleanings and treatments to maintain your pet\'s oral health.',
                'icon': 'tooth'
            },
            {
                'name': 'Surgery',
                'description': 'Various surgical procedures from routine spay/neuter to more complex operations.',
                'icon': 'scissors'
            },
            {
                'name': 'Emergency Care',
                'description': 'Immediate medical attention for urgent situations and injuries.',
                'icon': 'alert-circle'
            },
            {
                'name': 'Laboratory Services',
                'description': 'Diagnostic tests to help identify health issues and monitor treatment progress.',
                'icon': 'flask'
            },
            {
                'name': 'Grooming',
                'description': 'Professional grooming services to keep your pet clean and comfortable.',
                'icon': 'scissors'
            },
            {
                'name': 'Nutrition Counseling',
                'description': 'Expert advice on your pet\'s dietary needs for optimal health.',
                'icon': 'utensils'
            }
        ]
        
        for service_data in services_data:
            Service.objects.get_or_create(
                name=service_data['name'],
                defaults={
                    'description': service_data['description'],
                    'icon': service_data['icon']
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded services'))
        
        # Create sample clinics if none exist
        if Clinic.objects.count() == 0:
            clinics_data = [
                {
                    'name': 'Pawsome Pet Clinic',
                    'address': '123 Main St, Anytown, USA',
                    'phone': '(555) 123-4567',
                    'email': 'info@pawsome.example.com',
                    'description': 'A full-service veterinary clinic dedicated to providing the highest quality care for your pets.'
                },
                {
                    'name': 'Happy Tails Veterinary Center',
                    'address': '456 Oak Ave, Somewhere, USA',
                    'phone': '(555) 987-6543',
                    'email': 'care@happytails.example.com',
                    'description': 'Compassionate care for all your furry, feathered, and scaly friends.'
                },
                {
                    'name': 'Healthy Pets Clinic',
                    'address': '789 Pine Rd, Elsewhere, USA',
                    'phone': '(555) 456-7890',
                    'email': 'hello@healthypets.example.com',
                    'description': 'Modern veterinary care with a focus on preventative medicine and wellness.'
                }
            ]
            
            services = list(Service.objects.all())
            
            for clinic_data in clinics_data:
                clinic = Clinic.objects.create(
                    name=clinic_data['name'],
                    address=clinic_data['address'],
                    phone=clinic_data['phone'],
                    email=clinic_data['email'],
                    description=clinic_data['description']
                )
                
                # Assign random services to each clinic
                import random
                clinic_services = random.sample(services, random.randint(3, len(services)))
                clinic.services.set(clinic_services)
            
            self.stdout.write(self.style.SUCCESS('Successfully loaded sample clinics'))
        
        # Create a superuser if none exists
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpassword'
            )
            self.stdout.write(self.style.SUCCESS('Created superuser: admin / adminpassword'))