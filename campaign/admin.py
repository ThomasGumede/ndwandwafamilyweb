from django.contrib import admin
from campaign.models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    pass

