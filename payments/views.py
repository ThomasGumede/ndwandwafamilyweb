import hashlib
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from orders.models import ContributionOrder, TicketOrder, PaymentStatus
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
import base64
import hmac

header = {
            "Authorization": "Bearer sk_test_481ace6anmqyVgm55ac4a4f92a6f",
            "Content-Type": "application/json"
        }

def decimal_to_str(dec_value):
    # Returns a decimal to string and removes a comma
    return f"{dec_value}".replace(".", "")

def generateExpectedSignature(signed_content, secret):
    secret_bytes = base64.b64decode(secret.split('_')[1])
    hmac_signature = hmac.new(secret_bytes, signed_content.encode(), hashlib.sha256).digest()
    expected_signature = base64.b64encode(hmac_signature).decode()

    return expected_signature

def webhookRequest(request):
    data = json.dumps({
                "name": "Ndwandwafam_signals",
                "url": request.build_absolute_uri(reverse("payments:payment-webhook"))
            })
    response = requests.request("POST", "https://payments.yoco.com/api/webhooks", data=data, headers=header)
    return response


class WebhookView(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            
            webhook_id = request.META["webhook-id"]
            timestamp = request.META["webhook-timestamp"]
            signatures = request.META["webhook-signature"]
            signed_content = str(webhook_id) + '.' + str(timestamp) + '.' + str(request.body)
            response = webhookRequest(request)
            response.raise_for_status()
            new_response = response.json()
            secret = new_response["secret"]
            signature = signatures.split(' ')[0].split(',')[1]
            expected_signature = generateExpectedSignature(signed_content, secret=secret)
            if hmac.compare_digest(signature, expected_signature):
                return HttpResponse(status=200)
            
            
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.HTTPError:
            return HttpResponse(status=400)
        
        data = request.POST

# Create your views here.
class ContributionOrderProcessView(LoginRequiredMixin, View):
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

        # convert decimal to str and remove . 
        str_amount = decimal_to_str(self.model.amount)
        
        session_data = {
            'successUrl': success_url,
            'cancelUrl': cancel_url,
            "failureUrl": fail_url,
            'amount': int(str_amount),
            'currency': 'ZAR',
            'metadata': {
                "checkoutId": f"{self.model.donateid}"
            },
            "lineitems": [
                {"name": self.model.campaign.title,
                "description": "Contribution to campaign"}
            ]

        }
        data = json.dumps(session_data)

        
        try:
            response = requests.request("POST", "https://payments.yoco.com/api/checkouts", data=data, headers=header)
            response.raise_for_status()
            response_dat = response.json()
            return redirect(response_dat["redirectUrl"])

        except requests.ConnectionError as err:
            return render(request, "payment/timeout.html", {"err": err})
        except requests.HTTPError as err:
            return render(request, "payment/error.html", {"message": "Your payment was not processed due to internal error from our payment system, Please try again later"})

class ContributionOrderPaid(View):
    def get(self, request, *args, **kwargs):
        return render(request, "payment/contribution/success.html")
    
class ContributionOrderFailed(View):
    def get(self, request, *args, **kwargs):
        return render(request, "payment/contribution/fail.html")
    
class ContributionOrderCancelled(View):
    def get(self, request, *args, **kwargs):
        return render(request, "payment/contribution/cancelled.html")
    

class TicketOrderProcessView(LoginRequiredMixin, View):
    model = None
    template_name = "payment/tickets/payment.html"
    def dispatch(self, request, ticket_id, *args, **kwargs):
        self.model = get_object_or_404(TicketOrder, id=ticket_id)
        return super().dispatch(request, ticket_id,*args, **kwargs)
    

    def get(self, request, ticket_id,*args, **kwargs):
        return render(request, self.template_name, {"ticketorder": self.model})

    def post(self, request, ticket_id, *args, **kwargs):
        success_url = request.build_absolute_uri(reverse("payments:ticket-payment-success"))
        cancel_url = request.build_absolute_uri(reverse("payments:ticket-payment-cancelled"))
        fail_url = request.build_absolute_uri(reverse("payments:ticket-payment-failed"))

        # convert decimal to str and remove . 
        str_amount = decimal_to_str(self.model.total_price)
        str_amount_per_ticket = decimal_to_str(self.model.event.ticket_price)
        
        session_data = {
            'successUrl': success_url,
            'cancelUrl': cancel_url,
            "failureUrl": fail_url,
            'amount': int(str_amount),
            'currency': 'ZAR',
            'metadata': {
                "checkoutId": f"{self.model.ticketorderid}"
            },
            "lineItems": [
                {
                    "displayName": self.model.event.title,
                    "quantity": self.model.quantity,
                    "pricingDetails": {
                        "price": int(str_amount_per_ticket)
                    }
                }
            ]

        }
        data = json.dumps(session_data)

        
        try:
            response = requests.request("POST", "https://payments.yoco.com/api/checkouts", data=data, headers=header)
            print(response.json())
            response.raise_for_status()
            response_dat = response.json()
            return redirect(response_dat["redirectUrl"])

        except requests.ConnectionError as err:
            pass
        except requests.HTTPError as err:
            print(err)
            return render(request, "payment/error.html", {"message": "Your payment was not processed due to internal error from our payment system, Please try again later"})
        


class TicketOrderPaid(View):
    def get(self, request, *args, **kwargs):
        return render(request, "payment/tickets/success.html")
    
class TicketOrderCancelled(View):
    def get(self, request, *args, **kwargs):
        return render(request, "payment/tickets/cancelled.html")

    
class TicketOrderFailed(View):
    def get(self, request, *args, **kwargs):
        return render(request, "payment/tickets/fail.html")
    

   