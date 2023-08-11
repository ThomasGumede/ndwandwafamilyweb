import uuid
from django.urls import reverse
from utils.file_upload_helper import handle_event_file_upload, handle_post_file_upload
from django.db import models
from campaign.models import Category, in_fourteen_days
from accounts.models import Address
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.utils.translation import gettext as _
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify

class Event(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    image = models.ImageField(help_text=_("Upload campaign image."), upload_to=handle_event_file_upload,blank=True, null=True)
    title = models.CharField(help_text=_("Enter title for your event"), max_length=150)
    slug = models.SlugField(max_length=250, blank=True, unique=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None, related_name="events")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="events")
    content = models.TextField()
    is_ticket_sold = models.BooleanField(_("Tickets will be sold?"), default=False)
    ticket_price = models.DecimalField(help_text=_("Enter ticket price"), max_digits=1000, decimal_places=2, default=0.00)
    event_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name="events", blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    event_date = models.DateTimeField(default=in_fourteen_days)
    tags = TaggableManager(blank=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        pass

    def save(self, *args, **kwargs):
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
        return reverse("event:event_details", kwargs={"slug": self.slug})

class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    image = models.ImageField(help_text=_("Upload news image."), upload_to=handle_post_file_upload, blank=True, null=True)
    title = models.CharField(help_text=_("Enter title for your post"), max_length=150)
    slug = models.SlugField(max_length=250, blank=True, unique=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="posts")
    content = models.TextField()
    tags = TaggableManager(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def save(self, *args, **kwargs):
        original_slug = slugify(self.title)
        queryset =  Post.objects.all().filter(slug__iexact=original_slug).count()

        count = 1
        slug = original_slug
        while(queryset):
            slug = original_slug + '-' + str(count)
            count += 1
            queryset = Post.objects.all().filter(slug__iexact=slug).count()

        self.slug = slug
        super(Post, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title}"
    
    def get_absolute_url(self):
        return reverse("event:post_details", kwargs={"slug": self.slug})

@receiver(pre_delete, sender=Event)
def delete_event_image_hook(sender, instance, using, **kwargs):
    instance.image.delete()

@receiver(pre_delete, sender=Post)
def delete_Post_image_hook(sender, instance, using, **kwargs):
    instance.image.delete()

