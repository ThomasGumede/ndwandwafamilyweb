from django.shortcuts import render
from django.views.generic import TemplateView, View
from campaign.models import Campaign
from event.models import Event
from news.models import Post
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

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

class EmailTemplateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "email.html")
    
class SearchView(View):
    template_name = "home/search/search.html"
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", None)
        query_by = request.GET.get("search_in", None)

        if query and query_by:
            match query_by:
                case "campaigns":
                    results = Campaign.objects.filter(title__icontains = query)
                    results_type = "campaigns"
                case "events":
                    results = Event.objects.filter(title__icontains = query)
                    results_type = "events"
                case "posts":
                    results = Post.objects.filter(title__icontains = query)
                    results_type = "posts"
                case "accounts":
                    results = User.objects.filter(Q(username__icontains = query) | Q(first_name__icontains = query) | Q(last_name__icontains = query) | Q(occupation__icontains = query))
                    results_type = "accounts"
                case _:
                    results = Campaign.objects.filter(title__icontains = query)
                    results_type = "campaigns"
        else:
            results = None
            results_type = None

        return render(request, self.template_name, {"results": results, "results_type": results_type, "query": query, "query_by": query_by})