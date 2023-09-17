import uuid

def handle_profile_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return f"profile/{filename}"

def handle_verification_docs_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}-{}.{}'.format(uuid.uuid4().hex, instance.user.username,ext)
    return f"profile/verify/{filename}"

def handle_campaign_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return f"campaign/{filename}"

def handle_post_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return f"post/{filename}"

def handle_event_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return f"event/{filename}"