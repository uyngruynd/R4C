from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from customers.models import Customer
from robots.models import Robot


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5, blank=False, null=False)

    # Признак того, что заказ находится в режиме ожидания поступления робота
    is_pending = models.BooleanField()


@receiver(pre_save, sender=Order)
def set_pending(sender, instance, **kwargs):
    """
    Перед записью нового заказа вычисляю признак ожидания исходя из учтенных
     и не проданных роботов с соответствующим серийным номером.
    """
    if instance.pk is None:
        instance.is_pending = Robot.objects.filter(
            serial=instance.robot_serial, sold__isnull=True).count() == 0
