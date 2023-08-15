from typing import Any
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from event.models import Event
from accounts.forms import AddressForm
from accounts.models import Address
from event.forms import EventForm
from campaign.models import Category
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import DetailView, View, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
import datetime

class EventListView(View):
    model = Event
    template_name = "event/events.html"

    def get(self, request, category_id=None,*args, **kwargs):
        days = datetime.timedelta(days=14) + timezone.now()
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            queryset = self.model.objects.filter(category = category).order_by("-created").select_related("author")
        else:
            queryset = self.model.objects.filter(event_startdate__range=[timezone.now(), days]).order_by("-created").select_related("author")

        return render(request, self.template_name, {"events": queryset})
    
class EventDetailView(DetailView):
    
    queryset = Event.objects.order_by("-created").select_related("author", "event_address")
    template_name = "event/event.html"
    context_object_name = "event"

    slug_field = 'slug'
    slug_url_kwarg = 'event_slug'

class EventCreateView(LoginRequiredMixin, View):
    model = Event
    form_class = EventForm
    template_name = "event/create_form.html"
    extra_form_class = AddressForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form" : self.form_class, "form2": self.extra_form_class})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        form2 = self.extra_form_class(request.POST)
        if form.is_valid() and form.is_multipart() and form2.is_valid():
            
            event_clean = form.cleaned_data
            if event_clean["event_address"]:
                address_real = Address.objects.get(id=event_clean["event_address"])
            else:
                address_real = None
                
            instance = form.save(commit=False)
            instance.author = request.user

            if address_real != None:
                instance.event_address = address_real
            else:
                address = form2.save()
                instance.event_address = address
                
            
            
            event = instance.save()
            
            messages.success(request, f"Event {instance.title} was created successfully")
            return redirect("event:event_details", event_slug=instance.slug)
        else:
            messages.error(request, "Error while trying to create event")
            return render(request, self.template_name, {"form" : form, "form2": form2})
    

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

        if self.model == None or self.model.author != request.user:
            return JsonResponse(data={"success": False, "message": "Event not found"}, status=404)
        
        return super().dispatch(request, event_uuid=event_uuid, *args, **kwargs)
    
    def post(self, request, event_uuid, *args, **kwargs):
        if self.model != None:
            self.model.delete()
            return JsonResponse(data = {'success': True, "message": "Event deleted successfully", "url": reverse_lazy("event:event_list")}, status=200)
        else:
            return JsonResponse(data={"success": False, "message": "Something went wrong on our side, event was not removed", "url": reverse_lazy("event:event_list")}, status=500)
    

