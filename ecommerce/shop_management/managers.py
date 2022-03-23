from django.db.models import Manager


class ShopManager(Manager):
    def get_queryset(self):
        return super(ShopManager, self).get_queryset().all().exclude(status="deleted")


class ConfirmedShopManager(Manager):
    def get_queryset(self):
        return (
            super(ConfirmedShopManager, self).get_queryset().filter(status="confirmed")
        )
