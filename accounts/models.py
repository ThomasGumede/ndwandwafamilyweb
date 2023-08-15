from typing import Any
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.core.validators import RegexValidator
from django.urls import reverse

PHONE_REGEX = RegexValidator(
    r'^(\+27|0)[6-8][0-9]{8}$', 'RSA phone number is required')

class Address(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    address_one = models.CharField(max_length=300)
    address_two = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    country = models.CharField(max_length=300, default="South Africa")
    zipcode = models.BigIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def __str__(self):
        return f"{self.address_one} {self.city} {self.state}"

    def get_absolute_url(self):
        return reverse("accounts:address", kwargs={"id": self.id})
    
class Wallet(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    name = models.CharField(max_length=250)
    balance = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    amount_donated = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    owner = models.OneToOneField("CustomUser", on_delete=models.CASCADE, related_name="my_wallet")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("accounts:wallet", kwargs={"id": self.id})

class CustomUser(AbstractUser):
    class Title(models.TextChoices):
        MR = ("MR", "Mr")
        MRS = ("MRS", "Mrs")
        MS = ("MS", "Miss")
        DR = ("DR", "Doctor")
        PROF = ("PROF", "Professor")
        ADVOCATE = ("ADVOCATE", "Adv")
        CLLR = ("CLLR", "Cllr")
        OTHER = ("OTHER", "Other")
        
    title = models.CharField(max_length=10, choices=Title.choices, default=Title.OTHER)
    
    photo = models.ImageField(_("Upload profile image"), upload_to="profile/", null=True, blank=True)
    tel = models.CharField(_("Enter your cellphone number"), max_length=15, validators=[PHONE_REGEX], unique=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    id_number = models.CharField(help_text=_("Enter your 13 digits ID number"), max_length=13, blank=True, null=True)
    biography = models.TextField(blank=True)
    occupation = models.CharField(_("Enter your current employment"), max_length=500, blank=True, null=True)
    professional_affiliations = models.CharField(_("Enter your professional affiliations"), max_length=700, blank=True, null=True)
    following = models.ManyToManyField('self', through='Contact', symmetrical=False, related_name='followers', blank=True)
    created = models.DateTimeField(auto_now_add=True)



    class Meta:
        verbose_name = _("Accounts")
        verbose_name_plural = _("Accounts")
        ordering = ["-created"]
    
    def email_user(self, subject: str, message: str, sender: str, **kwargs: Any) -> None:
        return super().email_user(subject, message, sender, **kwargs)
    
    def get_absolute_url(self):
        return reverse("accounts:account_details", kwargs={"username": self.username, "pk": self.pk})
    
    
    def __str__(self) -> str:
        return f"{self.username} {self.last_name}"
    
class NextOfKin(models.Model):
    class RelationShip(models.TextChoices):
        OTHER = ("OTHER", "Other")
        WIFE = ("WIFE", "Wife")
        HUSBAND = ("HUSBAND", "Husband")
        DAUGHTER = ("DAUGHTER", "Daughter")
        SON = ("SON", "Son")
        MOTHER = ("MOTHER", "Mother")
        FATHER = ("FATHER", "Father")
        GRANDMOTHER = ("GRANDMOTHER", "Grandmother")
        GRANDFATHER = ("GRANDFATHER", "Grandfather")
        BROTHER = ("BROTHER", "Brother")
        SISTER = ("SISTER", "Sister")
        COUSIN = ("COUSIN", "Cousin")
        AUNT = ("AUNT", "Aunt")
        UNCLE = ("UNCLE", "Uncle")

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    full_name = models.CharField(_("Enter your relatives name's"), max_length=300)
    relationship = models.CharField(max_length=300, choices=RelationShip.choices, default=RelationShip.OTHER)
    tel = models.CharField(_("Enter relative's cell phone number"), max_length=15,  validators=[PHONE_REGEX])
    relative = models.ForeignKey(CustomUser, related_name="next_of_kins", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    

class Qualification(models.Model):
    class QualificationType(models.TextChoices):
        BACHELOR = ("BACHELOR", "Bachelor's Degree")
        MASTER = ("MASTER", "Master's Degree")
        DOCTORAL = ("DOCTORAL", "Doctoral Degree")
        POSTGRAD = ("POSTGRAD_CERT", "Postgraduate Certificate")
        HIGH_CERT = ("HIGH_CERTI", "Higher Certicate")
        ADVA_DIP = ("ADVANCE_DIP", "Advance Diploma")
        DIPLOMA = ("DIPLOMA", "Diploma")
        HONO = ("HONOURS", "Honour's Degree")
        MATRIC = ("MATRIC", "Grade 12 Matric")
        OTHER = ("OTHER", "Other")

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    institution = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    qualification_type = models.CharField(max_length=300, choices=QualificationType.choices, default=QualificationType.MATRIC)
    year = models.CharField(max_length=50, help_text="Enter year range e.g 2019 - 2022")
    owner = models.ForeignKey(CustomUser, related_name="qualifications", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        pass

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("accounts:qualification", kwargs={"id": self.id})


class Contact(models.Model):
    user_from = models.ForeignKey(CustomUser, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(CustomUser, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'

# Signals for deleting object file from memory disk
@receiver(pre_delete, sender=CustomUser)
def delete_content_files_hook(sender, instance, using, **kwargs):
	instance.photo.delete()

