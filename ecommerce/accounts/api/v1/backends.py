from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        else:
            return None

    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None


class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(phone_number=email)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        else:
            return None

    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
