from django.contrib.auth.backends import BaseBackend
from gestionPatient.models import Medecin

class AuthMedecin(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Medecin.objects.get(email=username)
            if user.check_password(password):
                return user
        except Medecin.DoesNotExist:
            return None
    def get_user(self,user_id):
        try:
            return Medecin.objects.get(id=user_id)
        except Medecin.DoesNotExist:
            return None
