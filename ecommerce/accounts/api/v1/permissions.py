from accounts.models import CustomUser as User
from django.db.models import Q


class PhoneNumberVerificationPermission:
    def has_permission(self, request, view):
        user = User.objects.filter(
            Q(email=request.data["email"]) | Q(phone_number=request.data["email"])
        ).first()
        if user:
            if user.passed_phone_number_verification:
                return True
            else:
                return False
        else:
            return False
