from django.contrib import admin
from campaign.models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

class CampaignReportInline(admin.TabularInline):
    model = CampaignReport

class DonationInline(admin.TabularInline):
    model = Donation

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    pass

@admin.register(CampaignReport)
class CampaignReportAdmin(admin.ModelAdmin):
    pass
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass

# Register your models here.
