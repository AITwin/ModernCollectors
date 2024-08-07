from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask

from collectors.models import Source


@receiver(post_save, sender=Source)
def sync_periodic_tasks(sender, instance, **kwargs):
    if instance.task:
        instance.task.delete()
    if instance.enabled and instance.interval_schedule:
        task = PeriodicTask.objects.create(
            name=f"{instance.storage_slug} - {instance.group}",
            task="collectors.tasks.collect",
            interval=instance.interval_schedule,
            args=[instance.id],
        )
        # Prevents infinite recursion of the signal
        Source.objects.filter(pk=instance.pk).update(task=task)
