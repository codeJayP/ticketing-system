from django.db import models
from django.contrib.auth.models import User, Group
import uuid
from django.db.models import Count

# Create your models here.
    
class Department(models.Model):
    name = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return self.name
    
class Office(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name
    
class KindOfEquipment(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class RepairDescription(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class RepairRequest(models.Model):
    STATUS_CHOICES = (
        ('ongoing', 'Ongoing'),
        ('complete', 'Complete'),
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description_staff = models.ForeignKey(RepairDescription, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    equip_type = models.ForeignKey(KindOfEquipment, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=600, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    property_num = models.IntegerField(unique=True, null=True, blank=True)
    serial_num = models.IntegerField(unique=True, null=True, blank=True)
    kind_of_work = models.CharField(max_length=500, blank=True, null=True)
    complete = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    staff_id = 1


    def __str__(self):
         return f"{self.office}"
    
    def save(self, *args, **kwargs):
        if self.first_name:
            self.first_name = self.first_name.upper()
        if self.last_name:
            self.last_name = self.last_name.upper()
        super().save(*args, **kwargs)
    #set data to upper()
    
class TicketLogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    logs = models.CharField(max_length=150, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

