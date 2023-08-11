from typing import Any
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models.query import QuerySet
from django.http import HttpResponse
from event.models import Event
from event.forms import EventForm
from campaign.models import Category
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import DetailView, View, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class EventListView(View):
    model = Event
    template_name = "event/events.html"

    def get(self, request, category_id=None,*args, **kwargs):
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            queryset = self.model.objects.filter(category = category).order_by("-created").select_related("author")
        else:
            queryset = self.model.objects.order_by("-created").select_related("author")

        return render(request, self.template_name, {"events": queryset})
    
class EventDetailView(DetailView):
    model = Event
    queryset = model.objects.order_by("-created").select_related("author", "category", "tags")
    template_name = "event/event.html"
    context_object_name = "event"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

class EventCreateView(LoginRequiredMixin, FormView):
    model = Event
    form_class = EventForm
    template_name = "event/create_form.html"

    def form_invalid(self, form):
        messages.error("Event was not created, please fix below errors")
        return super(EventCreateView, self).form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        messages.success("Event created successfully")
        return super(EventCreateView, self).form_valid(form)
    

class EventUpdateView(LoginRequiredMixin, View):
    model = None
    template_name = "event/update_form.html"
    form_class = EventForm

    def dispatch(self, request, event_id, *args, **kwargs):
        self.model = get_object_or_404(Event, id=event_id)
        if self.model.author != request.user:
            return HttpResponseForbidden("You are not allowed to perform this task")
        return super().dispatch(request, event_id,*args, **kwargs)
    
    def get(self, request, event_id, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class(instance=self.model)})
    
    def post(self, request, event_id, *args, **kwargs):
        form = self.form_class(request.POST, request.FILE, instance=self.model)
        if form.is_valid() and form.is_multipart():
            form.save()
            return redirect("event:event_details", slug = self.model.slug)
        return render(request, self.template_name, {"form": self.form_class(instance=self.model)})

class EventDeleteView(LoginRequiredMixin, View):
    model = None

    def dispatch(self, request, event_uuid, *args, **kwargs):
        self.model = Event.objects.get(id = event_uuid)

        if self.model == None or self.model.creator.pk != request.user.pk:
            return JsonResponse(data={"success": False, "message": "Event not found"}, status=404)
        
        return super().dispatch(request, event_uuid=event_uuid, *args, **kwargs)
    
    def post(self, request, event_uuid, *args, **kwargs):
        if self.model != None:
            self.model.delete()
            return JsonResponse(data = {'success': True, "message": "Event deleted successfully"}, status=200)
        else:
            return JsonResponse(data={"success": False, "message": "Something went wrong on our side, event was not removed"}, status=500)
    

