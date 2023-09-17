from django import forms
from event.models import Event
from tinymce.widgets import TinyMCE

class EventForm(forms.ModelForm):
    event_address = forms.UUIDField(required=False)
    class Meta:
        model = Event
        fields = ["image", "title", "content", "ticket_price", "event_startdate", "tags", "event_enddate"]

        widgets = {
            
            'event_startdate': forms.DateTimeInput(attrs={"type": "datetime-local", "class": "border-0 px-3 py-3 {% if form.end_date.errors %} border-2 border-red-500{% endif %} placeholder-blueGray-300 text-gray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"}),
            'tags': forms.DateTimeInput(attrs={"type": "text", "class": "border-0 px-3 py-3 {% if form.tags.errors %} border-2 border-red-500{% endif %} placeholder-blueGray-300 text-gray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"}),
            'content': TinyMCE(attrs={"class": "border-0 px-3 py-3 {% if form.content.errors %} h-44 border-2 border-red-500{% endif %} placeholder-gray-300 text-gray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150", "rows": 8}),
            'event_enddate': forms.DateTimeInput(attrs={"type": "datetime-local", "class": "border-0 px-3 py-3 {% if form.end_date.errors %} border-2 border-red-500{% endif %} placeholder-blueGray-300 text-gray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"})
        }

