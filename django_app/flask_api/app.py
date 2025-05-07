from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from .resources import (
    AppointmentListResource,
    AppointmentResource,
    ServiceListResource,
    ServiceResource,
    ReviewListResource,
    ReviewResource,
    ClinicReviewsResource,
    UserReviewsResource,
    ClinicServicesResource,
    HealthCheckResource
)

app = Flask(__name__)
CORS(app)
api = Api(app)

# Register API resources
api.add_resource(AppointmentListResource, '/api/appointments')
api.add_resource(AppointmentResource, '/api/appointments/<int:appointment_id>')
api.add_resource(ServiceListResource, '/api/services')
api.add_resource(ServiceResource, '/api/services/<int:service_id>')
api.add_resource(ReviewListResource, '/api/reviews')
api.add_resource(ReviewResource, '/api/reviews/<int:review_id>')
api.add_resource(ClinicReviewsResource, '/api/clinics/<int:clinic_id>/reviews')
api.add_resource(UserReviewsResource, '/api/users/<int:user_id>/reviews')
api.add_resource(ClinicServicesResource, '/api/clinics/<int:clinic_id>/services')
api.add_resource(HealthCheckResource, '/api/health')

if __name__ == '__main__':
    app.run(debug=True, port=5000)