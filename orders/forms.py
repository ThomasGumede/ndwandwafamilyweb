from django import forms
from orders.models import TicketOrder, ContributionOrder

class TicketOrderForm(forms.ModelForm):
    
    class Meta:
        model = TicketOrder
        fields = ("accepted_laws", "quantity", "phone", "email")

class ContributionOrderForm(forms.ModelForm):
    class Meta:
        model = ContributionOrder
        fields = ("amount", "accepted_laws")

class ContributionForm(forms.Form):
    anonymous = forms.BooleanField(help_text="Contribute anonymously?")
    amount = forms.IntegerField(help_text="Enter contribution amount")