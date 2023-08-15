import uuid
from datetime import timedelta
import datetime
from utils.file_upload_helper import handle_campaign_file_upload
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.models import  GenericUUIDTaggedItemBase, TaggedItemBase
from django.utils.translation import gettext as _
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model
from accounts.models import Wallet

User = get_user_model()

def in_fourteen_days():
    return timezone.now() + timedelta(days=14)



class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    label = models.CharField(max_length=250, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name_plural = "Categories"


class Campaign(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    image = models.ImageField(help_text=_("Upload campaign image."), upload_to=handle_campaign_file_upload,blank=True, null=True)
    title = models.CharField(help_text=_("Enter title for your campaign"), max_length=150)
    slug = models.SlugField(max_length=250, blank=True)
    details = models.TextField(help_text=_("Enter additional details about your campaign"), max_length=2000)
    target = models.DecimalField(help_text=_("Enter target amount, max 1000"), max_digits=1000, decimal_places=2, default=0.00)
    current_amount = models.DecimalField(help_text=_("Enter amount you currently have"), max_digits=1000, decimal_places=2, default=0.00)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=in_fourteen_days)
    creation_date = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="campaigns")
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = TaggableManager(blank=True, through=UUIDTaggedItem)
    

    def get_days(self):
        date = self.end_date - self.start_date
        print(date.seconds)
        if date.days == 0:
            return f"{date} hours"
        return f"{date.days} days"

    def get_percentage_of_donated_fund(self):
        val = self.current_amount / self.target
        perc = val * 100
        return round(perc, 2)
    

    def __str__(self):
        return str(self.title)
    
    def save(self, *args, **kwargs):
        original_slug = slugify(self.title)
        queryset =  Campaign.objects.all().filter(slug__iexact=original_slug).count()

        count = 1
        slug = original_slug
        while(queryset):
            slug = original_slug + '-' + str(count)
            count += 1
            queryset = Campaign.objects.all().filter(slug__iexact=slug).count()

        self.slug = slug

        wallet = get_object_or_404(Wallet, owner = self.creator)
        wallet.balance += self.current_amount
        wallet.save(update_fields=["balance"])
        super(Campaign, self).save(*args, **kwargs)

    errors = {}

    def clean(self):
        if (self.is_featured == True and Campaign.objects.filter(is_featured=True).exclude(id=self.id).count() >= 5):
            raise ValidationError(
                {'is_featured': _('You already have five featured campaigns.')})

        valid = True
        start_date = self.start_date
        end_date = self.end_date
        self.errors = {}
        if str(start_date) < str(datetime.date.today()):
            self.errors['date'] = 'invalid date'
            valid = False
        elif str(end_date) == str(start_date):
            self.errors['date'] = 'invalid date'
            valid = False
        elif str(end_date) < str(start_date):
            self.errors['date'] = 'invalid date'
            # 'End date should be greater than start date.'
            valid = False
        elif str(end_date) == str(datetime.date.today()):
            self.errors['date'] = 'invalid date'
            valid = False
        if self.title == '':
            self.errors['title'] = 'title is required'
            valid = False
        if self.details == '':
            self.errors['details'] = 'details is required'
            valid = False
        if self.target == '':
            self.errors['target'] = 'target is required'
            valid = False
        return valid


class CampaignReport(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    details = models.TextField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.details)


class Rating(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    value = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.value)

    class Meta:
        unique_together = ('campaign', 'user',)


class Donation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    amount = models.DecimalField(max_digits=1000, decimal_places=2)
    additional_statement = models.TextField(blank=True, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="donations")
    donator = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, related_name="donations")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)
    
    def save(self, *args, **kwargs):
        wallet = get_object_or_404(Wallet, owner = self.donator)
        self.campaign.current_amount += self.amount
        self.campaign.save(update_fields=["current_amount"])
        wallet.amount_donated += self.amount
        wallet.save(update_fields=["amount_donated"])
        super().save(self, *args, **kwargs)


@receiver(pre_delete, sender=Campaign)
def delete_campaign_image_hook(sender, instance, using, **kwargs):
    instance.image.delete()
