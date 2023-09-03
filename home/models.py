from django.db import models

class AboutUs(models.Model):
    content = models.TextField()

class TeamMember(models.Model):
    image = models.ImageField()
    full_name = models.CharField(max_length=300)