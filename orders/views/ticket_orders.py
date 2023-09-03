from decimal import Decimal
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from event.models import Event
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from accounts.models import Address
from orders.forms import TicketOrderForm


class TicketBuyView(LoginRequiredMixin, View):
    model = None
    form_class = TicketOrderForm
    quantity = 1
    total_price = 0
    email = None
    phone = None
    template_name = "orders/tickets/ticket_order_summary.html"
    
    def dispatch(self, request, event_id, *args, **kwargs):
        self.model = get_object_or_404(Event, id=event_id)
        self.quantity = request.GET.get("quantity", 1)
        self.email = request.GET.get("email", request.user.email)
        self.phone = request.GET.get("phone", request.user.tel)
        self.total_price = Decimal(self.quantity) * self.model.ticket_price
        return super().dispatch(request, event_id, *args, **kwargs)
    
    def get(self, request, event_id, *args, **kwargs):
        context = {"form": self.form_class, "quantity": self.quantity, "email": self.email, "phone": self.phone, "total": self.total_price, "event": self.model}
        return render(request, self.template_name, context)

    def post(self, request, event_id, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ticketorder = form.save(commit=False)
            ticketorder.buyer = request.user
            ticketorder.event = self.model
            ticketorder.save()
            return redirect("payments:tickets-order", ticket_id=ticketorder.id)
        else:
            context = {"form": form, "quantity": self.quantity, "email": self.email, "phone": self.phone, "total": self.total_price, "event": self.model}
            return render(request, self.template_name, context)
            

            

