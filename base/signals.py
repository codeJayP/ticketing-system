
# code
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
 
 
@receiver(post_save, sender=RepairRequest)
def create_profile(sender, instance, created, **kwargs):
    try:
        system_log = f"RR{instance.date.strftime('%Y')}{instance.id} Assign to {instance.staff} requested by {instance.first_name}"
        logs = TicketLogs(logs=system_log)
        logs.save()
        if logs.id:
            print(logs.id)
    except Exception as e:
        print(str(e))

