from django.db.models.signals import pre_save
from django.dispatch import receiver

from friday_meals.models import Order


@receiver(pre_save, sender=Order)
def default_week_number(sender, instance, **kwargs):
    if instance.date:
        instance.weekNumber = instance.date.isocalendar()[1]

pre_save.connect(default_week_number, sender=Order)
