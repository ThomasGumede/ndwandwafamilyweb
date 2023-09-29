from django.core.mail import EmailMessage
from decimal import Decimal
from campaign.models import Campaign
from orders.models import ContributionOrder
from django.contrib.auth import get_user_model
from orders.forms import ContributionOrderForm
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.template.loader import render_to_string
User = get_user_model()

def ContributionConfirmEmail(request, user: User, to_email, order_id):
    
    try:
        order = ContributionOrder.objects.get(id=order_id)
        mail_subject = "Contribution Confirmation."
        message = render_to_string("email/contribution/contribution_confirm.html", {
            'user': user.get_full_name(),
            'donate_id': order.donateid,
            'campaign': order.campaign.title,
            "amount": order.amount,
        })
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.content_subtype = 'html'
        if email.send():
            messages.success(request, f'Confirmation was sent to {to_email}')
        else:
            messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
    except ContributionOrder.DoesNotExist:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
    

class ContributionCreateView(LoginRequiredMixin, View):
    campaign = None
    template_name = "orders/contribution/contribution_summary.html"
    form_class = ContributionOrderForm
    check = "on"
    amount = 50
    
    
    def dispatch(self, request, campaign_id,*args, **kwargs):
        self.campaign = get_object_or_404(Campaign, id=campaign_id)
        self.check = request.GET.get("accepted", "on")
        self.amount = request.GET.get("amount", 50)
        return super().dispatch(request, campaign_id,*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        context = {
            "campaign": self.campaign,
            "form": self.form_class,
            "checked": self.check,
            "amount": self.amount
        }
        return render(request, self.template_name, context)
    

    def post(self, request, campaign_id, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.campaign = self.campaign
            instance.contributor = request.user
            instance.save()
            ContributionConfirmEmail(request, request.user, request.user.email, instance.id)
            messages.success(request, f"Your donation was added successfully, Thank you!")
            return redirect("payments:contribution-order", donation_id =instance.id)
        else:
            context = {
                "campaign": self.campaign,
                "form": form,
                "checked": self.check,
                "amount": self.amount
            }
            messages.error(request, f"Your donation was not added successfully, Sorry!")
            return render(request, self.template_name, context)
    
class DonationCancelView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, 'donation_email.html')
    