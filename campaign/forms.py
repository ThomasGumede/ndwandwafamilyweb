from django import forms
from campaign.models import Category, Campaign, Donation

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('label',)

class DonationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=300)
    last_name  = forms.CharField(max_length=300)
    address_one  = forms.CharField(max_length=300)
    address_two = forms.CharField(max_length=300)
    city = forms.CharField(max_length=300)
    state = forms.CharField(max_length=300)
    country = forms.CharField(max_length=300)
    zipcode = forms.IntegerField(min_value=0) 
    class Meta:
        model = Donation
        fields = ("amount", "additional_statement")

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ("category", "title", "details", "target", "current_amount", "start_date", "end_date", "image")

        widgets = {
            'start_date': forms.DateTimeInput(attrs={"type": "datetime-local", "class": "border-0 px-3 py-3 {% if form.end_date.errors %} border-2 border-red-500{% endif %} placeholder-blueGray-300 text-gray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"}),
            'end_date': forms.DateTimeInput(attrs={"type": "datetime-local", "class": "border-0 px-3 py-3 {% if form.end_date.errors %} border-2 border-red-500{% endif %} placeholder-blueGray-300 text-gray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"})
        }

