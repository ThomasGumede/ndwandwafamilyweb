import datetime
import uuid
from utils.file_upload_helper import handle_event_file_upload
from django.db import models
from campaign.models import in_fourteen_days
from django.template.defaultfilters import slugify
from accounts.models import AddressModel
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.utils.translation import gettext as _
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.utils import timezone
from campaign.models import UUIDTaggedItem
from django.core.validators import RegexValidator
from django.urls import reverse
from tinymce.models import HTMLField

PHONE_REGEX = RegexValidator(r'^(\+27|0)[6-8][0-9]{8}$', 'RSA phone number is required')


class Event(models.Model):
    image = models.ImageField(help_text=_("Upload campaign image."), upload_to=handle_event_file_upload,blank=True, null=True)
    title = models.CharField(help_text=_("Enter title for your event"), max_length=150)
    slug = models.SlugField(max_length=250, blank=True, unique=True)
    organiser = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None, related_name="events")
    content = HTMLField()
    event_address = models.ForeignKey(AddressModel, on_delete=models.SET_NULL, related_name="events", blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    available_seates = models.PositiveIntegerField(default=0)
    event_link = models.URLField(blank=True, null=True)
    event_online = models.BooleanField(default=False)
    event_startdate = models.DateTimeField(default=timezone.now)
    event_enddate = models.DateTimeField(default=in_fourteen_days)
    tags = TaggableManager(blank=True, through=UUIDTaggedItem)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        pass

    def save(self, *args, **kwargs):
        self.full_clean()
        original_slug = slugify(self.title)
        queryset =  Event.objects.all().filter(slug__iexact=original_slug).count()

        count = 1
        slug = original_slug
        while(queryset):
            slug = original_slug + '-' + str(count)
            count += 1
            queryset = Event.objects.all().filter(slug__iexact=slug).count()

        self.slug = slug
        super(Event, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title}"
    
    def get_absolute_url(self):
        return reverse("event:event_details", kwargs={"event_slug": self.slug})

class EventTicketTypeModel(models.Model):
    title = models.CharField(max_length=250, help_text=_("Enter ticket type"))
    available_seats = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    event = models.ForeignKey(Event, related_name="tickettypes", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        super(EventTicketTypeModel, self).save(*args, **kwargs)


@receiver(pre_delete, sender=Event)
def delete_event_image_hook(sender, instance, using, **kwargs):
    instance.image.delete()



