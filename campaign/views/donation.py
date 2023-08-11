from typing import Any
from django.http import HttpResponse
from campaign.models import Donation, Campaign
from campaign.forms import DonationForm
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, View, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class DonationListView(View):
    model = Donation
    template_name = "donation/donations.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"donations": self.model.objects.all()})
    
class DonationCreateView(LoginRequiredMixin, FormView):
    model = Donation
    template_name = "donation/create.html"
    form_class = DonationForm

    def form_invalid(self, form) -> HttpResponse:
        messages.error("Something went wrong, please fix below errors")
        return super(DonationCreateView, self).form_invalid(form)
    
    def form_valid(self, form) -> HttpResponse:
        campaign = get_object_or_404(Campaign, id=self.kwargs["campaign_id"])
        form.instance.campaign = campaign
        form.instance.donator = self.request.user
        form.save()
        messages.success("Donation added successfully, pending verification")
        return super(DonationCreateView, self).form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse("campaign:campaign_details", campaign_id=self.kwargs["campaign_id"])