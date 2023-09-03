from django.urls import path
from event.views.event import *
from event.views.post import *


app_name = "event"

urlpatterns = [
    path("all_events", EventListView.as_view(), name="event_list"),
    path("event_details/<slug:event_slug>", EventDetailView.as_view(), name="event_details"),
    path("update/<event_id>", EventUpdateView.as_view(), name="event_update"),
    path("delete/<event_uuid>", EventDeleteView.as_view(), name="delete_event"),
    path("create_event", EventCreateView.as_view(), name="create_event"),

    path("all_posts", PostListView.as_view(), name="post_list"),
    path("all_posts/<category_id>", PostListView.as_view(), name="post_list_by_category"),
    path("post_details/<slug:post_slug>", PostDetailView.as_view(), name="post_details")
]
