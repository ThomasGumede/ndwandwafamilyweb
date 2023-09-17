from typing import Any
from utils.file_upload_helper import handle_profile_upload, handle_verification_docs_upload
from utils.validators import verify_rsa_phone
from utils.choices import *
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.core.validators import RegexValidator
from django.urls import reverse

PHONE_VALIDATOR = verify_rsa_phone()

class AddressModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    address_one = models.CharField(max_length=300)
    address_two = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=300)
    province = models.CharField(max_length=300)
    country = models.CharField(max_length=300, default="South Africa")
    zipcode = models.BigIntegerField()
    address_id = models.CharField(max_length=300, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Addresses")
        verbose_name_plural = _("Addresses")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.address_one} {self.city} {self.state}"

    def get_absolute_url(self):
        return reverse("accounts:address", kwargs={"id": self.id})

class MailingGroupModel(models.Model):
   id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
   title = models.CharField(max_length=300, unique=True, db_index=True)
   description = models.CharField(help_text="Describe mailing list", max_length=500)

   def __str__(self):
       return self.title
   
   def send_email(self, message, subject, attachments=None):
      pass

class WalletModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    name = models.CharField(max_length=250)
    balance = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    owner = models.OneToOneField("CustomUserModel", on_delete=models.CASCADE, related_name="my_wallet")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("accounts:wallet", kwargs={"id": self.id})

class CustomUserModel(AbstractUser):
    title = models.CharField(max_length=10, choices=TitleChoices.choices, default=TitleChoices.OTHER)
    profile_image = models.ImageField(_("Upload profile image"), upload_to=handle_profile_upload, null=True, blank=True)
    phone = models.CharField(_("Enter your cellphone number"), max_length=15, validators=[PHONE_VALIDATOR], unique=True)
    address = models.OneToOneField(AddressModel, related_name="user_address", on_delete=models.CASCADE)
    biography = models.TextField(blank=True)
    occupation = models.CharField(_("Enter your current employment"), max_length=500, blank=True, null=True)
    professional_affiliations = models.CharField(_("Enter your professional affiliations"), max_length=700, blank=True, null=True)
    identity_choice = models.CharField(_("Select your identity document"), max_length=100, choices=IdentityNumberChoices.choices, default=IdentityNumberChoices.ID_NUMBER)
    identity_number = models.CharField(unique=True, max_length=13)
    verification_status = models.CharField(max_length=100, choices=VerificationChoices.choices, default=VerificationChoices.NOT_VERIFIED)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Accounts")
        verbose_name_plural = _("Accounts")
        ordering = ["-created"]
    
    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"username": self.username})
    
    def __str__(self) -> str:
        return f"{self.username} {self.last_name}"

class IdentityVerificationModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    identity_image =  models.ImageField(upload_to=handle_verification_docs_upload, null=False, help_text=_("Please take a selfie while holding an official identification document(ID Card, Passport, drivers license, etc)"))
    identitybook_image = models.ImageField(upload_to=handle_verification_docs_upload, null=False, help_text=_("Please take a picture of your official identification document(ID Card, Passport, drivers license, etc)"))
    user = models.OneToOneField(CustomUserModel, related_name="verification", on_delete=models.CASCADE)

    class Meta:
        pass

    def get_absolute_url(self):
        return reverse("accounts:identity", kwargs={"id": self.id, "username": self.user.get_username()})
    
    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - Identity verification data"

class RelativeModel(models.Model):
    full_name = models.CharField(_("Enter your relatives name's"), max_length=300)
    relationship = models.CharField(max_length=300, choices=RelationShip.choices, default=RelationShip.OTHER)
    phone = models.CharField(_("Enter relative's cell phone number"), max_length=15,  validators=[PHONE_VALIDATOR], unique=True, null=True, blank=True)
    relative = models.ForeignKey(CustomUserModel, related_name="relatives", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def get_absolute_url(self):
        return reverse("accounts:relative", kwargs={"id": self.id})
    
    def __str__(self):
        return self.full_name
    
class QualificationModel(models.Model):
    institution = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    qualification_type = models.CharField(max_length=300, choices=QualificationType.choices, default=QualificationType.MATRIC)
    year = models.CharField(max_length=50, help_text="Enter year range e.g 2019 - 2022")
    owner = models.ForeignKey(CustomUserModel, related_name="qualifications", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("accounts:qualification", kwargs={"id": self.id})
    

    class Meta:
        pass

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("accounts:qualification", kwargs={"id": self.id})

@receiver(pre_delete, sender=CustomUserModel)
def delete_content_files_hook(sender, instance, using, **kwargs):
	instance.profile_image.delete()

@receiver(pre_delete, sender=IdentityVerificationModel)
def delete_content_files_hook(sender, instance, using, **kwargs):
	instance.identity_image.delete()
	instance.identitybook_image.delete()

class Subscribe(models.Model):
    user = models.ForeignKey(CustomUserModel, related_name="subscriber", on_delete=models.CASCADE)
    mailinggroup = models.ForeignKey(MailingGroupModel, related_name="subscribe_to", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)


