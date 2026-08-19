from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import NPA, NPAStatusHistory


@receiver(pre_save, sender=NPA)
def track_npa_status_change(sender, instance, **kwargs):

    if not instance.pk:
        return

    try:
        old_instance = NPA.objects.get(pk=instance.pk)
    except NPA.DoesNotExist:
        return

    if old_instance.recovery_status != instance.recovery_status:

        NPAStatusHistory.objects.create(
            npa=instance,
            old_status=old_instance.recovery_status,
            new_status=instance.recovery_status
        )