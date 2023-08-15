from django import forms
from event.models import Event, Post

class EventForm(forms.ModelForm):
    event_address = forms.UUIDField(required=False)
    class Meta:
        model = Event
        fields = ["image", "title", "content", "ticket_price", "event_startdate", "tags", "event_enddate"]

        widgets = {
            
            'event_startdate': forms.DateTimeInput(attrs={"type": "datetime-local", "class": "border-0 px-3 py-3 {% if form.end_date.errors %} border-2 border-red-500{% endif %} placeholder-blueGray-300 text-gray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"}),
            'event_enddate': forms.DateTimeInput(attrs={"type": "datetime-local", "class": "border-0 px-3 py-3 {% if form.end_date.errors %} border-2 border-red-500{% endif %} placeholder-blueGray-300 text-gray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"})
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "image", "content", "category", "tags"]