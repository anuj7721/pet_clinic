from datetime import datetime

class AppointmentModel:
    """
    Model class for appointments in the Flask API
    This is a simple in-memory model since we're using a JSON file for storage
    """
    
    def __init__(self, id, pet_id, clinic_id, date, time, reason, status="PENDING", created_at=None):
        self.id = id
        self.pet_id = pet_id
        self.clinic_id = clinic_id
        self.date = date
        self.time = time
        self.reason = reason
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()
    
    def to_dict(self):
        """Convert the model to a dictionary for JSON serialization"""
        return {
            'id': self.id,
            'pet_id': self.pet_id,
            'clinic_id': self.clinic_id,
            'date': self.date,
            'time': self.time,
            'reason': self.reason,
            'status': self.status,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a model instance from a dictionary"""
        return cls(
            id=data.get('id'),
            pet_id=data.get('pet_id'),
            clinic_id=data.get('clinic_id'),
            date=data.get('date'),
            time=data.get('time'),
            reason=data.get('reason'),
            status=data.get('status', 'PENDING'),
            created_at=data.get('created_at')
        )


class ServiceModel:
    """
    Model class for services in the Flask API
    """
    
    def __init__(self, id, name, description, icon=None):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
    
    def to_dict(self):
        """Convert the model to a dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a model instance from a dictionary"""
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            icon=data.get('icon')
        )


class ReviewModel:
    """
    Model class for reviews in the Flask API
    """
    
    def __init__(self, id, user_id, clinic_id, rating, comment, created_at=None):
        self.id = id
        self.user_id = user_id
        self.clinic_id = clinic_id
        self.rating = rating
        self.comment = comment
        self.created_at = created_at or datetime.now().isoformat()
    
    def to_dict(self):
        """Convert the model to a dictionary for JSON serialization"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'clinic_id': self.clinic_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a model instance from a dictionary"""
        return cls(
            id=data.get('id'),
            user_id=data.get('user_id'),
            clinic_id=data.get('clinic_id'),
            rating=data.get('rating'),
            comment=data.get('comment'),
            created_at=data.get('created_at')
        )