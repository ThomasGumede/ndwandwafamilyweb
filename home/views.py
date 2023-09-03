from django.shortcuts import render
from django.views.generic import TemplateView, View
from campaign.models import Campaign
from event.models import Event, Post

class HomeView(View):
    template_name = "home/home.html"

    def get(self, request, *args, **kwargs):
        events = Event.objects.all().order_by("-created")[:3]
        campaigns = Campaign.objects.all().order_by("-creation_date")[:3]
        news = Post.objects.all()[:3]
        context = {
            "events" : events,
            "campaigns": campaigns,
            "news": news
        }
        return render(request, self.template_name, context)
