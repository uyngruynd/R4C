from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from services.mailing_service import CustomersMailing


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)

    # Добавил поле для регистрации события продажи робота, проданные роботы
    # не учитываются при получении признака is_pending нового заказа
    sold = models.DateTimeField(null=True)


@receiver(post_save, sender=Robot)
def customers_mailing(sender, instance, created, **kwargs):
    """Вызов сервиса почтовой рассылки для ожидающих поступления товара."""
    if created:
        mailing = CustomersMailing(instance.serial)
        mailing.execute()
