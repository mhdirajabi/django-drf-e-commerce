from datetime import timedelta

from django.db import models
from django.utils import timezone


class TOTPRequestQuerySet(models.QuerySet):
    def is_valid(self, receiver, request, code):
        current_time = timezone.now()
        result = self.filter(
            receiver=receiver,
            request_id=request,
            code=code,
            created__lt=current_time,
            created__gt=current_time - timedelta(seconds=300),
        ).exists()
        return result
