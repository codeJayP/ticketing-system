from django.contrib import admin
from .models import *

admin.site.register(Office)
admin.site.register(RepairRequest)
admin.site.register(Department)
admin.site.register(KindOfEquipment)
admin.site.register(TicketLogs)