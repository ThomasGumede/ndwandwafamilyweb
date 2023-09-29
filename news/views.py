from typing import Any
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from news.models import Post
from campaign.models import Category
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import DetailView, View

class PostListView(View):
    model = Post
    template_name = "news/news.html"

    def get(self, request, category_id=None,*args, **kwargs):
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            queryset = self.model.objects.filter(category = category).order_by("-created").select_related("author")
        else:
            queryset = self.model.objects.all().order_by("-created").select_related("author")

        return render(request, self.template_name, {"posts": queryset})
    
class PostDetailView(DetailView):
    
    queryset = Post.objects.order_by("-created").select_related("author", "category")
    template_name = "news/news-details.html"
    context_object_name = "post"

    slug_field = 'slug'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_posts"] = Post.objects.order_by("-created").only("title", "image", "event_startdate")[:5]
        return context
    
