from django.contrib import admin
from accounts.models import *

@admin.register(CustomUserModel)
class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(QualificationModel)
class QualificationAdmin(admin.ModelAdmin):
    pass

@admin.register(AddressModel)
class AddressAdmin(admin.ModelAdmin):
    pass
@admin.register(MailingGroupModel)
class MailingAdmin(admin.ModelAdmin):
    pass


@admin.register(RelativeModel)
class RelativeAdmin(admin.ModelAdmin):
    pass

@admin.register(WalletModel)
class WalletAdmin(admin.ModelAdmin):
    pass

# Register your models here.
