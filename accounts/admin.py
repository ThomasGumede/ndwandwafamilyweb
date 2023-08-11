from django.contrib import admin
from accounts.models import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    pass

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(NextOfKin)
class NextOfKinAdmin(admin.ModelAdmin):
    pass

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass

# Register your models here.
