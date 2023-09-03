from django import forms
from campaign.models import Category, Campaign
from tinymce.widgets import TinyMCE

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('label',)

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ("category", "title", "details", "target", "end_date", "image")

        widgets = {
            'details': TinyMCE(attrs={"class": "border-0 px-3 py-3 {% if form.details.errors %} h-44 border-2 border-red-500{% endif %} placeholder-gray-300 text-gray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150", "rows": 8}),
            'end_date': forms.DateTimeInput(attrs={"type": "datetime-local", "class": "border-0 px-3 py-3 {% if form.end_date.errors %} border-2 border-red-500{% endif %} placeholder-blueGray-300 text-gray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"})
        }

