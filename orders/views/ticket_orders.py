from decimal import Decimal
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model
from event.models import Event
from orders.models import TicketOrder
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.template.loader import render_to_string
from orders.forms import TicketOrderForm
User = get_user_model()

def orderConfirmEmail(request, user: User, to_email, order_id):
    try:
        order = TicketOrder.objects.get(id=order_id)
        mail_subject = "Activate your user account."
        message = render_to_string("email/tickets/order_confirmation.html", {
            'user': user.get_full_name(),
            'order_number': order.ticketorderid,
            'event_title': order.event.title,
            'order_quantity': order.quantity,
            "ticket_amount": order.event.ticket_price,
            "order_total_price": order.total_price
        })
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.content_subtype = 'html'
        if email.send():
            messages.success(request, f'Confirmation was sent to {to_email}')
        else:
            messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
    except TicketOrder.DoesNotExist:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


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
            orderConfirmEmail(request, request.user, request.user.email, ticketorder.id)
            return redirect("payments:tickets-order", ticket_id=ticketorder.id)
        else:
            context = {"form": form, "quantity": self.quantity, "email": self.email, "phone": self.phone, "total": self.total_price, "event": self.model}
            return render(request, self.template_name, context)
            

            

