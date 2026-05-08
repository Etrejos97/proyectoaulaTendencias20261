from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Task, TaskHistory

TRACKED_FIELDS = ['status', 'priority', 'assigned_to_id']


@receiver(pre_save, sender=Task)
def track_task_changes(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return

    changed_by = getattr(instance, '_changed_by', None)

    for field in TRACKED_FIELDS:
        old_val = getattr(old, field)
        new_val = getattr(instance, field)

        if old_val != new_val:
            if field == 'assigned_to_id':
                old_display = old.assigned_to.username if old.assigned_to else 'Sin asignar'
                new_display = instance.assigned_to.username if instance.assigned_to else 'Sin asignar'
                field_name = 'assigned_to'
            else:
                old_display = str(old_val) if old_val else ''
                new_display = str(new_val) if new_val else ''
                field_name = field

            TaskHistory.objects.create(
                task=instance,
                changed_by=changed_by,
                field_changed=field_name,
                old_value=old_display,
                new_value=new_display,
            )