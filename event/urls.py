from django.urls import path
from event.views import *


app_name = "event"

urlpatterns = [
    path("all_events", EventListView.as_view(), name="event_list"),
    path("event_details/<slug:event_slug>", EventDetailView.as_view(), name="event_details"),
    path("update/<event_id>", EventUpdateView.as_view(), name="event_update"),
    path("delete/<event_uuid>", EventDeleteView.as_view(), name="delete_event"),
    path("create_event", EventCreateView.as_view(), name="create_event"),
]
