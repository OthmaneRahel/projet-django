from django.contrib.auth.backends import BaseBackend
from gestionPatient.models import Patient

class AuthPatient(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Patient.objects.get(email=username)
            if user.check_password(password):
                return user
        except Patient.DoesNotExist:
            return None
    def get_user(self,user_id):
        try:
            return Patient.objects.get(id=user_id)
        except Patient.DoesNotExist:
            return None
