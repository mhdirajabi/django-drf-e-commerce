from django.db import models


class PaidCartsManager(models.Manager):
    def get_queryset(self):
        return super(PaidCartsManager, self).get_queryset().filter(status="paid")


class CancelledCartsManager(models.Manager):
    def get_queryset(self):
        return (
            super(CancelledCartsManager, self).get_queryset().filter(status="cancelled")
        )


class OtherCartsManager(models.Manager):
    def get_queryset(self):
        return (
            super(OtherCartsManager, self)
            .get_queryset()
            .all()
            .filter(models.Q(status="processing") | models.Q(status="confirmed"))
        )
