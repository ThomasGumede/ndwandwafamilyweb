from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from orders.models import ContributionOrder, TicketOrder, PaymentStatus
from decimal import Decimal
import json
from django.core.mail import EmailMessage
import requests

# Create your views here.
class ContributionOrderProcessView(View):
    model = None
    template_name = "payment/contribution/payment.html"

    def dispatch(self, request, donation_id,*args, **kwargs):
        self.model = get_object_or_404(ContributionOrder, id=donation_id)
        return super().dispatch(request, donation_id,*args, **kwargs)
    

    def get(self, request, donation_id,*args, **kwargs):
        return render(request, self.template_name, {"donation": self.model})

    def post(self, request, donation_id, *args, **kwargs):
        success_url = request.build_absolute_uri(reverse("payments:contribution-payment-success"))
        cancel_url = request.build_absolute_uri(reverse("payments:contribution-payment-cancelled"))
        fail_url = request.build_absolute_uri(reverse("payments:contribution-payment-failed"))
        session_data = {
            
            'metadata': f"{self.model.donateid}",
            'successUrl': success_url,
            'cancelUrl': cancel_url,
            "fail": fail_url,
            'amount': f"{self.model.amount}",
            'currency': 'ZAR',
        }
        header = {
            "Authorization": "Bearer sk_live_54e8d7c8nmqyVgm851f48399baec",
            "Content-Type": "application/json"
        }
        data = requests.post("https://payments.yoco.com/api/checkouts", json=session_data, headers=header)
        print(data)

        return render(request, self.template_name, {"donation": self.model})

class ContributionOrderPaid(View):
    def get(self, request, *args, **kwargs):
        return render(request, "payment/contribution/success.html")
    
class ContributionOrderFailed(View):
    def get(self, request, *args, **kwargs):
        return render(request, "payment/contribution/fail.html")
    
class ContributionOrderCancelled(View):
    def get(self, request, *args, **kwargs):
        return render(request, "payment/contribution/cancelled.html")
    

class TicketOrderProcessView(View):
    model = None
    template_name = "payment/ticket/payment.html"
    def dispatch(self, request, ticket_id, *args, **kwargs):
        self.model = get_object_or_404(TicketOrder, id=ticket_id)
        return super().dispatch(request, ticket_id,*args, **kwargs)
    

    def get(self, request, ticket_id,*args, **kwargs):
        return render(request, self.template_name, {"ticketorder": self.model})

    def post(self, request, ticket_id, *args, **kwargs):
        self.model.paid = PaymentStatus.PENDING
        self.model.save(update_fields=["paid"])
        self.model.campaign.current_amount += self.model.amount
        self.model.campaign.save(update_fields=["current_amount"])


class TicketOrderPaid(View):
    def get(self, request, *args, **kwargs):
        return render(request, "payment/ticket/success.html")
    
class TicketOrderCancelled(View):
    def get(self, request, *args, **kwargs):
        return render(request, "payment/ticket/cancelled.html")

        return render(request, self.template_name, {"ticketorder": self.model})