from django.http import request
from campaign.models import Category

def categories(request):
    categories = Category.objects.all()
    return {"categories" : categories}