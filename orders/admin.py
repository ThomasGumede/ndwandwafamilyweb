from django.contrib import admin
from orders.models import *

# Register your models here.
@admin.register(ContributionOrder)
class ContributionOrderAdmin(admin.ModelAdmin):
    pass
@admin.register(TicketOrder)
class TicketOrderAdmin(admin.ModelAdmin):
    pass