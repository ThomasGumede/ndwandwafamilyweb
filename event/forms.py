from django import forms
from event.models import Event, Post

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["image", "title", "category", "content", "is_ticket_sold", "ticket_price", "event_date", "tags"]