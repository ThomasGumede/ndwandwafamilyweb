import os
import uuid

def handle_profile_upload(instance, filename):
    return f"profile/myimage_{instance.pk}/{filename}"

def handle_campaign_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return f"campaign/myimage_{instance.id}/{filename}"

def handle_post_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return f"post/myimage_{instance.id}/{filename}"

def handle_event_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return f"event/myimage_{instance.id}/{filename}"