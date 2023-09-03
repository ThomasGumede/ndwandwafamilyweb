from django.urls import path
from actions.views.user_actions import FollowUser
from actions.views.search import SearchView

app_name = "actions"
urlpatterns = [
    path("", SearchView.as_view(), name="search_results"),
    path('follow', FollowUser.as_view(), name='follow_user'),
]
