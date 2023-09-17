import uuid
from utils.file_upload_helper import handle_post_file_upload
from django.db import models
from campaign.models import Category
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.utils.translation import gettext as _
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from campaign.models import UUIDTaggedItem
from django.urls import reverse
from tinymce.models import HTMLField


# Create your models here.
class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    image = models.ImageField(help_text=_("Upload news image."), upload_to=handle_post_file_upload, blank=True, null=True)
    title = models.CharField(help_text=_("Enter title for your news"), max_length=150)
    slug = models.SlugField(max_length=250, blank=True, unique=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="posts")
    content = HTMLField()
    tags = TaggableManager(blank=True, through=UUIDTaggedItem)
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
        return reverse("event:post_details", kwargs={"post_slug": self.slug})
    

@receiver(pre_delete, sender=Post)
def delete_Post_image_hook(sender, instance, using, **kwargs):
    instance.image.delete()