from decimal import Decimal
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from event.models import EventTicketOrder, Event
from django.views.generic import DetailView, View, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from accounts.models import Address
from event.forms import TicketOrderForm
from accounts.forms import AddressForm


class TicketBuyView(LoginRequiredMixin, View):
    model = None
    form_class = TicketOrderForm
    extra_form = AddressForm
    quantity = 1
    template_name = "tickets/checkout_summary.html"
    def dispatch(self, request, event_id, *args, **kwargs):
        self.model = get_object_or_404(Event, id=event_id)
        
        return super().dispatch(request, event_id, *args, **kwargs)
    
    def get(self, request, event_id, *args, **kwargs):
        quantity = request.GET.get("quantity", None)
        if quantity != None:
            self.quantity = quantity

        total_price = Decimal(quantity) * self.model.ticket_price
        return render(request, self.template_name, {"form": self.form_class, "form2": self.extra_form, "quantity": self.quantity, "total": total_price, "event": self.model})

    def post(self, request, event_id, *args, **kwargs):
        form = self.form_class(request.POST)
        form2 = self.extra_form(request.POST)
        if form.is_valid() and form2.is_valid():
            cd = form.cleaned_data
            if cd["billing_address"]:
                address = get_object_or_404(Address, id=cd["billing_address"])
            else:
                address = form2.save()
            
            ticketorder = form.save(commit=False)
            ticketorder.buyer = request.user
            ticketorder.event = self.model
            ticketorder.billing_address = address
            ticketorder.save()
            # instance.save()

            return redirect("actions:processevent_payment", ticket_id=ticketorder.id)
        else:
            return render(request, self.template_name, {"form": form, "form2": form2})
            

            

