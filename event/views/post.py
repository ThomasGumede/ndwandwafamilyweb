from typing import Any
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from event.models import Post
from accounts.forms import AddressForm
from event.forms import PostForm
from campaign.models import Category
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import DetailView, View, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
import datetime

class PostListView(View):
    model = Post
    template_name = "post/posts.html"

    def get(self, request, category_id=None,*args, **kwargs):
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            queryset = self.model.objects.filter(category = category).order_by("-created").select_related("author")
        else:
            queryset = self.model.objects.all().order_by("-created").select_related("author")

        return render(request, self.template_name, {"posts": queryset})
    
class PostDetailView(DetailView):
    
    queryset = Post.objects.order_by("-created").select_related("author", "category")
    template_name = "post/post.html"
    context_object_name = "post"

    slug_field = 'slug'
    slug_url_kwarg = 'post_slug'

class PostCreateView(LoginRequiredMixin, View):
    model = Post
    form_class = PostForm
    template_name = "post/create_form.html"
    

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form" : self.form_class})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        
        if form.is_valid() and form.is_multipart():
 
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            
            messages.success(request, f"Post {instance.title} was created successfully")
            return redirect("post:post_details", post_slug=instance.slug)
        else:
            messages.error(request, "Error while trying to create post")
            return render(request, self.template_name, {"form" : form})
    

class PostUpdateView(LoginRequiredMixin, View):
    model = None
    template_name = "post/update_form.html"
    form_class = PostForm

    def dispatch(self, request, post_id, *args, **kwargs):
        self.model = get_object_or_404(Post, id=post_id)
        if self.model.author != request.user:
            return HttpResponseForbidden("You are not allowed to perform this task")
        return super().dispatch(request, post_id,*args, **kwargs)
    
    def get(self, request, post_id, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class(instance=self.model)})
    
    def post(self, request, post_id, *args, **kwargs):
        form = self.form_class(request.POST, request.FILE, instance=self.model)
        if form.is_valid() and form.is_multipart():
            form.save()
            return redirect("post:post_details", slug = self.model.slug)
        return render(request, self.template_name, {"form": self.form_class(instance=self.model)})

class PostDeleteView(LoginRequiredMixin, View):
    model = None

    def dispatch(self, request, post_uuid, *args, **kwargs):
        self.model = Post.objects.get(id = post_uuid)

        if self.model == None or self.model.author != request.user:
            return JsonResponse(data={"success": False, "message": "Post not found"}, status=404)
        
        return super().dispatch(request, post_uuid=post_uuid, *args, **kwargs)
    
    def post(self, request, post_uuid, *args, **kwargs):
        if self.model != None:
            self.model.delete()
            return JsonResponse(data = {'success': True, "message": "Post deleted successfully", "url": reverse_lazy("post:post_list")}, status=200)
        else:
            return JsonResponse(data={"success": False, "message": "Something went wrong on our side, post was not removed", "url": reverse_lazy("post:post_list")}, status=500)
    

