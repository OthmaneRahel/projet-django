from django.contrib.auth.backends import BaseBackend
from gestionPatient.models import Secretaire

class AuthSecretaire(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Secretaire.objects.get(email=username)
            if user.check_password(password):
                return user
        except Secretaire.DoesNotExist:
            return None
    def get_user(self,user_id):
        try:
            return Secretaire.objects.get(id=user_id)
        except Secretaire.DoesNotExist:
            return None
