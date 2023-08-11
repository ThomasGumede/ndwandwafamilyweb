from django.urls import path
from event.views.event import *

app_name = "event"

urlpatterns = [
    path("events", EventListView.as_view(), name="event_list"),
    path("events/<category_id>", EventListView.as_view(), name="event_list_by_category"),
    path("events/<slug>", EventDetailView.as_view(), name="event_details"),
    path("events/update/<event_id>", EventUpdateView.as_view(), name="event_update"),
    path("events/create_event", EventCreateView.as_view(), name="create_event")
]
