from django.contrib import admin
from event.models import Event, Post

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
