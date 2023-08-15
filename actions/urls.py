from django.urls import path
from actions.views import UserSearchView

app_name = "actions"
urlpatterns = [
    path("", UserSearchView.as_view(), name="search_results")
]
